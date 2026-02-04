import json
from pathlib import Path

CHUNK_DIR = Path("src/data/chunks")
META_FILE = Path("src/data/chunks_metadata.json")

def main():
    metadata = []

    chunk_files = sorted(CHUNK_DIR.glob("*.txt"))
    print(f"Found {len(chunk_files)} chunk files")

    for chunk_file in chunk_files:
        name = chunk_file.stem
        # example: EnterpriseRAG_xxx_chunk_12
        if "_chunk_" in name:
            source, chunk_id = name.rsplit("_chunk_", 1)
        else:
            source, chunk_id = name, "0"

        metadata.append({
            "chunk_file": chunk_file.name,
            "source_file": source + ".txt",
            "chunk_id": int(chunk_id)
        })

    META_FILE.write_text(json.dumps(metadata, indent=2))
    print(f"Metadata saved → {META_FILE}")

if __name__ == "__main__":
    main()
