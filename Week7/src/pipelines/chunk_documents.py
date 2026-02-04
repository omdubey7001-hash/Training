from pathlib import Path
from src.utils.chunker import chunk_text

CLEAN_DIR = Path("src/data/cleaned")
CHUNK_DIR = Path("src/data/chunks")

CHUNK_DIR.mkdir(parents=True, exist_ok=True)

def main():
    files = list(CLEAN_DIR.glob("*.txt"))
    print(f"Found {len(files)} cleaned files")

    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            chunk_file = CHUNK_DIR / f"{file.stem}_chunk_{i}.txt"
            chunk_file.write_text(chunk, encoding="utf-8")

        print(f"{file.name} → {len(chunks)} chunks created")

if __name__ == "__main__":
    main()
