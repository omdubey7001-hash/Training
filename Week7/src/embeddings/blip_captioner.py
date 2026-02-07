import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class BLIPCaptioner:
    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(
            model_name
        ).to(self.device)

    def caption_image(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_length=50)

        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption
