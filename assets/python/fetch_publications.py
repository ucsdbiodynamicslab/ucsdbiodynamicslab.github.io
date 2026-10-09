import requests
import yaml
import time
import re
from pathlib import Path
from datetime import datetime
import os

API_KEY = os.environ.get("S2_API_KEY")

AUTHOR_IDS = [
    "2916647",
    "2245535793",
    "2367545890"
]

BASE_URL = "https://api.semanticscholar.org/graph/v1"

HEADERS = {
    "x-api-key": API_KEY,
    "User-Agent": "UCSD-Biodynamics-Lab-Publication-Bot"
}

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
OUTPUT_FILE = REPO_ROOT / "_data" / "biodynamics-lab" / "publications.yml"
EXCLUDE_FILE = REPO_ROOT / "_data" / "biodynamics-lab" / "publications_exclude.yml"

MIN_INTERVAL = 1.5
REQUEST_TIMEOUT = 30
MAX_RETRIES = 5
_last_request_time = 0


def wait_for_rate_limit():
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time

    if elapsed < MIN_INTERVAL:
        wait_time = MIN_INTERVAL - elapsed
        print(f"Waiting {wait_time:.2f}s...")
        time.sleep(wait_time)

    _last_request_time = time.time()


def rate_limited_get(session, url, params):
    backoff = 3

    for attempt in range(1, MAX_RETRIES + 1):
        wait_for_rate_limit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] GET {url}")

        try:
            response = session.get(url, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
        except (requests.ConnectionError, requests.Timeout) as e:
            problem = f"Network error ({e.__class__.__name__})"
        else:
            if response.status_code != 429 and response.status_code < 500:
                response.raise_for_status()
                return response
            problem = f"Hit {response.status_code}"

        if attempt == MAX_RETRIES:
            raise RuntimeError(f"{problem} on {url}; giving up after {MAX_RETRIES} attempts")

        print(f"{problem}. Sleeping {backoff} seconds and retrying ({attempt}/{MAX_RETRIES})...")
        time.sleep(backoff)
        backoff *= 2


def fetch_papers_for_author(session, author_id):
    papers = []
    offset = 0
    limit = 10
    page = 1

    print(f"\n=== Fetching papers for Author ID {author_id} ===\n")

    while True:
        url = f"{BASE_URL}/author/{author_id}/papers"
        params = {
            "limit": limit,
            "offset": offset,
            "fields": "paperId,title,authors,journal,publicationDate,year,url,externalIds"
        }

        print(f"Author {author_id} | Page {page} | Offset {offset}")
        response = rate_limited_get(session, url, params)
        data = response.json()

        batch = data.get("data", [])
        batch_size = len(batch)

        if batch_size == 0:
            print("No more papers for this author.")
            break

        papers.extend(batch)
        print(f"Retrieved {batch_size} | Running total: {len(papers)}\n")

        if batch_size < limit:
            print("Final page for this author.\n")
            break

        offset += limit
        page += 1

    return papers


def deduplicate_papers(all_papers):
    print("Deduplicating papers across author IDs...")
    unique = {}

    for paper in all_papers:
        paper_id = paper.get("paperId")
        if paper_id:
            unique[paper_id] = paper

    print(f"Unique papers after deduplication: {len(unique)}\n")
    return list(unique.values())


def resolve_link(paper):
    external_ids = paper.get("externalIds", {})
    doi = external_ids.get("DOI")

    if doi:
        return f"https://doi.org/{doi}"

    return paper.get("url")


def generate_pub_id(title):
    """Convert title to PascalCase pubID: split on special characters and capitalize each word"""
    # Treat non-alphanumeric characters as word breaks (matches existing pubIDs / PDF filenames)
    cleaned = re.sub(r'[^a-zA-Z0-9]', ' ', title)
    # Split by spaces and capitalize each word
    words = cleaned.split()
    # Join to create pubID
    pub_id = ''.join(word.capitalize() for word in words)
    return pub_id


def format_papers(papers):
    print("Formatting papers...")
    formatted = []

    for paper in papers:
        authors = [a["name"] for a in paper.get("authors", [])]
        journal_info = paper.get("journal")
        journal = journal_info.get("name") if journal_info else None
        title = paper.get("title")
        if not title:
            print(f"Skipping paper with no title: {paper.get('paperId')}")
            continue

        formatted.append({
            "title": title,
            "journal": journal,
            "authors": authors,
            "publication_date": paper.get("publicationDate"),
            "year": paper.get("year"),
            "link": resolve_link(paper),
            "pubID": generate_pub_id(title)
        })

    formatted.sort(key=lambda x: x.get("year") or 0, reverse=True)
    return formatted


def write_yaml(data, filename):
    print(f"Writing YAML to {filename}")
    filename.parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print("YAML write complete.\n")


def read_yaml_list(filename):
    """Read a YAML list, or [] if the file doesn't exist.

    Parse errors are raised rather than ignored: treating a broken publications.yml as
    empty would overwrite it and lose every pubID and manual edit.
    """
    if not filename.exists():
        return []

    with open(filename, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if data else []


def read_existing_publications(filename):
    """Read existing publications from YAML file"""
    return read_yaml_list(filename)


def read_excluded(filename):
    """Read the list of publications the bot should never add (by link and/or title)"""
    return read_yaml_list(filename)


def link_key(link):
    return (link or "").strip().lower() or None


def title_key(title):
    return generate_pub_id(title or "").lower() or None


def merge_publications(new_papers, existing_papers, excluded=()):
    """Merge fetched papers into the existing list.

    A fetched paper matches an existing entry by link (DOI) first, then by title ignoring
    case and punctuation. Matched entries are updated in place but keep their pubID, so
    PDF links don't break. Excluded papers are never added.
    """
    excluded_links = {link_key(e.get("link")) for e in excluded} - {None}
    excluded_titles = {title_key(e.get("title")) for e in excluded} - {None}

    # Start with existing papers
    merged = list(existing_papers)

    # Map links/titles to positions in merged (positions stay valid across replacements)
    index_by_link = {}
    index_by_title = {}
    for i, p in enumerate(merged):
        index_by_link.setdefault(link_key(p.get("link")), i)
        index_by_title.setdefault(title_key(p.get("title")), i)
    index_by_link.pop(None, None)
    index_by_title.pop(None, None)

    # Existing entries already updated during this merge
    claimed = set()

    # Handle link matches before title matches, so e.g. a published version can't take over
    # the entry of its preprint (same title) before the preprint itself is seen
    ordered = sorted(new_papers, key=lambda p: link_key(p.get("link")) not in index_by_link)

    # Add or update new papers
    for paper in ordered:
        link = link_key(paper.get("link"))
        title = title_key(paper.get("title"))

        if link in excluded_links or title in excluded_titles:
            print(f"Excluded: {paper.get('title')}")
            continue

        if link in index_by_link:
            idx = index_by_link[link]
            if idx in claimed:
                # Same link fetched twice: it's the same paper
                continue
        elif title in index_by_title and index_by_title[title] not in claimed:
            idx = index_by_title[title]
        else:
            idx = None

        if idx is not None:
            # Update existing paper with new data, keeping its pubID so PDF links don't break
            if merged[idx].get("pubID"):
                paper["pubID"] = merged[idx]["pubID"]
            merged[idx] = paper
            claimed.add(idx)
        else:
            # Add new paper. A paper whose title matches an already-updated entry (e.g. the
            # published version of a preprint) ends up with the same pubID and so the same PDF.
            print(f"New: {paper.get('title')}")
            idx = len(merged)
            merged.append(paper)
            claimed.add(idx)

        if link:
            index_by_link[link] = idx
        if title:
            index_by_title.setdefault(title, idx)

    # Sort by year descending
    merged.sort(key=lambda x: x.get("year") or 0, reverse=True)
    return merged


def main():
    start_time = time.time()
    print("=== UCSD Biodynamics Lab Publication Fetch ===\n")

    all_papers = []

    with requests.Session() as session:
        for author_id in AUTHOR_IDS:
            papers = fetch_papers_for_author(session, author_id)
            all_papers.extend(papers)

    print(f"\nTotal raw papers collected: {len(all_papers)}")

    unique_papers = deduplicate_papers(all_papers)
    formatted = format_papers(unique_papers)
    
    # Read existing publications and merge
    existing = read_existing_publications(OUTPUT_FILE)
    excluded = read_excluded(EXCLUDE_FILE)
    merged = merge_publications(formatted, existing, excluded)
    
    print(f"Total papers after merge: {len(merged)}\n")
    write_yaml(merged, OUTPUT_FILE)

    elapsed = round(time.time() - start_time, 2)
    print(f"Finished in {elapsed} seconds.")


if __name__ == "__main__":
    main()