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

MIN_INTERVAL = 1.5
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
    wait_for_rate_limit()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] GET {url}")
    response = session.get(url, headers=HEADERS, params=params)

    if response.status_code == 429:
        print("Hit 429. Sleeping 3 seconds and retrying...")
        time.sleep(3)
        return rate_limited_get(session, url, params)

    response.raise_for_status()
    return response


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
    """Convert title to camelCase pubID by removing special characters and capitalizing each word"""
    # Remove non-alphanumeric characters except spaces
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', title)
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


def read_existing_publications(filename):
    """Read existing publications from YAML file"""
    if not filename.exists():
        return []
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if data else []
    except Exception as e:
        print(f"Could not read existing publications: {e}")
        return []


def merge_publications(new_papers, existing_papers):
    """Merge new papers with existing ones, avoiding duplicates by title"""
    # Create a dict of existing papers indexed by title
    existing_by_title = {p.get("title"): p for p in existing_papers}
    
    # Start with existing papers
    merged = list(existing_papers)
    
    # Add or update new papers
    for paper in new_papers:
        title = paper.get("title")
        if title in existing_by_title:
            # Update existing paper with new data
            idx = merged.index(existing_by_title[title])
            merged[idx] = paper
        else:
            # Add new paper
            merged.append(paper)
    
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
    merged = merge_publications(formatted, existing)
    
    print(f"Total papers after merge: {len(merged)}\n")
    write_yaml(merged, OUTPUT_FILE)

    elapsed = round(time.time() - start_time, 2)
    print(f"Finished in {elapsed} seconds.")


if __name__ == "__main__":
    main()