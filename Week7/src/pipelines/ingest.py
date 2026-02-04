from pathlib import Path

RAW_ROOT = Path("src/data/raw/data_inside")
CLEAN_DIR = Path("src/data/cleaned")

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def main():
    md_files = list(RAW_ROOT.rglob("*.md"))

    print(f"Found {len(md_files)} markdown files")

    for md_file in md_files:
        # Text read karo
        text = md_file.read_text(encoding="utf-8", errors="ignore")

        if not text.strip():
            continue

        # Unique output name banao
        relative_path = md_file.relative_to(RAW_ROOT)
        safe_name = "_".join(relative_path.parts).replace(".md", ".txt")

        out_file = CLEAN_DIR / safe_name
        out_file.write_text(text, encoding="utf-8")

        print(f"Saved → {out_file}")

if __name__ == "__main__":
    main()
