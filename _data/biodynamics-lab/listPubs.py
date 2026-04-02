import yaml
import csv
import re
from pathlib import Path

def to_pascal_case(title: str) -> str:
    # Replace anything not alphanumeric with spaces
    cleaned = re.sub(r"[^a-zA-Z0-9]", " ", title)
    
    # Split into words, capitalize, and join
    words = cleaned.split()
    return "".join(word.capitalize() for word in words)

def main():
    input_file = Path("publications.yml")
    output_file = Path("publications_for_sheets.csv")

    # Load YAML
    with open(input_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["fileName", "title", "year", "link"])  # header

        for entry in data:
            title = entry.get("title", "").strip()
            if not title:
                continue
            
            pub_id = to_pascal_case(title)
            filename = f"{pub_id}.pdf"
            year = entry.get("year", "")
            link = entry.get("link", "")

            writer.writerow([filename, title, year, link])

    print(f"Exported to {output_file}")

if __name__ == "__main__":
    main()