import yaml
import re
from pathlib import Path
import shutil

def to_pascal_case(title: str) -> str:
    # Replace anything not alphanumeric with spaces
    cleaned = re.sub(r"[^a-zA-Z0-9]", " ", title)
    words = cleaned.split()
    return "".join(word.capitalize() for word in words)

def main():
    input_file = Path("publications.yml")
    backup_file = Path("publications.yml.bak")

    # Backup original file
    shutil.copy(input_file, backup_file)
    print(f"Backup created at {backup_file}")

    # Load YAML
    with open(input_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Update entries
    for entry in data:
        title = entry.get("title", "").strip()
        if not title:
            continue

        pub_id = to_pascal_case(title)
        entry["pubID"] = pub_id  # add or overwrite

    # Write back to YAML
    with open(input_file, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            sort_keys=False,      # preserve field order as much as possible
            allow_unicode=True    # keep names like O’Connor intact
        )

    print(f"Updated {input_file} with pubID fields")

if __name__ == "__main__":
    main()