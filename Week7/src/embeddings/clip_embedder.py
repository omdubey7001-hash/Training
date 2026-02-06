import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


class CLIPEmbedder:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

    def embed_image(self, image_path):
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        pixel_values = inputs["pixel_values"].to(self.device)

        with torch.no_grad():
            outputs = self.model.get_image_features(
                pixel_values=pixel_values
            )

        # ✅ GUARANTEED TENSOR EXTRACTION
        if hasattr(outputs, "pooler_output"):
            image_features = outputs.pooler_output
        else:
            image_features = outputs  # already tensor

        # ✅ SAFE NORMALIZATION
        image_features = image_features / image_features.norm(
            dim=-1, keepdim=True
        )

        return image_features.cpu().numpy()[0]

    def embed_text(self, text: str):
        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True
        )

        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model.get_text_features(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

        # outputs can be tensor or model output
        if hasattr(outputs, "pooler_output"):
            text_features = outputs.pooler_output
        else:
            text_features = outputs

        text_features = text_features / text_features.norm(
            dim=-1, keepdim=True
        )

        return text_features.cpu().numpy()
