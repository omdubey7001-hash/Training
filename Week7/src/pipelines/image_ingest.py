import json
import numpy as np
from pathlib import Path

from src.embeddings.clip_embedder import CLIPEmbedder
from src.embeddings.blip_captioner import BLIPCaptioner
from src.utils.ocr import extract_text

RAW_DIR = Path("src/data/raw/data_inside/EnterpriseRAG_2025_02_markdown")
EMB_DIR = Path("src/data/embeddings/images")
META_PATH = EMB_DIR / "image_metadata.json"

EMB_DIR.mkdir(parents=True, exist_ok=True)

def main():
    clip = CLIPEmbedder()
    blip = BLIPCaptioner()

    embeddings = []
    metadata = []

    for pdf_dir in RAW_DIR.iterdir():
        if not pdf_dir.is_dir():
            continue

        for img in pdf_dir.iterdir():
            if img.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                continue

            print(f"🖼 Processing image: {img}")

            # 1️⃣ CLIP embedding
            vec = clip.embed_image(str(img))
            embeddings.append(vec)

            # 2️⃣ BLIP caption
            caption = blip.caption(str(img))

            # 3️⃣ OCR text
            ocr_text = extract_text(str(img))

            metadata.append({
                "pdf": pdf_dir.name,
                "image_file": img.name,
                "image_path": str(img),
                "caption": caption,
                "ocr_text": ocr_text
            })

    np.save(EMB_DIR / "image_embeddings.npy", np.array(embeddings))

    with open(META_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ Stored {len(metadata)} images with CLIP + BLIP + OCR")

if __name__ == "__main__":
    main()
