import os
import json
import numpy as np
from pathlib import Path
from src.embeddings.clip_embedder import CLIPEmbedder

RAW_DIR = Path("src/data/raw/data_inside/EnterpriseRAG_2025_02_markdown")
EMB_DIR = Path("src/data/embeddings/images")
META_PATH = EMB_DIR / "image_metadata.json"

EMB_DIR.mkdir(parents=True, exist_ok=True)

def main():
    embedder = CLIPEmbedder()
    embeddings = []
    metadata = []

    for pdf_dir in RAW_DIR.iterdir():
        if not pdf_dir.is_dir():
            continue

        for file in pdf_dir.iterdir():
            if file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                print(f"Embedding image: {file}")

                vec = embedder.embed_image(file)
                embeddings.append(vec)

                metadata.append({
                    "pdf": pdf_dir.name,
                    "image_file": file.name,
                    "image_path": str(file)
                })

    embeddings = np.array(embeddings)
    np.save(EMB_DIR / "image_embeddings.npy", embeddings)

    with open(META_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ Saved {len(embeddings)} image embeddings")

if __name__ == "__main__":
    main()
