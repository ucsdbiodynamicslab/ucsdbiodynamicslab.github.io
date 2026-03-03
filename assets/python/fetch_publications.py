import requests
import yaml
import time
from pathlib import Path
from datetime import datetime

API_KEY = "jPcF0IbN4242Nvs7l2SJy9VSinrVjyIiEs8GLGFe"

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


def format_papers(papers):
    print("Formatting papers...")
    formatted = []

    for paper in papers:
        authors = [a["name"] for a in paper.get("authors", [])]
        journal_info = paper.get("journal")
        journal = journal_info.get("name") if journal_info else None

        formatted.append({
            "title": paper.get("title"),
            "journal": journal,
            "authors": authors,
            "publication_date": paper.get("publicationDate"),
            "year": paper.get("year"),
            "link": resolve_link(paper)
        })

    formatted.sort(key=lambda x: x.get("year") or 0, reverse=True)
    return formatted


def write_yaml(data, filename):
    print(f"Writing YAML to {filename}")
    filename.parent.mkdir(parents=True, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print("YAML write complete.\n")


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
    write_yaml(formatted, OUTPUT_FILE)

    elapsed = round(time.time() - start_time, 2)
    print(f"Finished in {elapsed} seconds.")


if __name__ == "__main__":
    main()