import os

os.environ["HF_DATASETS_OFFLINE"]="1"
os.environ["TRANSFORMERS_OFFLINE"]="1"

import litserve as ls
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import torch
from io import BytesIO


class PaliGemmaLitAPI(ls.LitAPI):
    def setup(self, device):
        model_id = "google/paligemma-3b-mix-224"
        self.model = PaliGemmaForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map=device,
            revision="bfloat16",
        ).eval()
        self.processor = AutoProcessor.from_pretrained(model_id)

    def decode_request(self, request):
        image_bytes = bytes.fromhex(request["image_bytes"])
        image = Image.open(BytesIO(image_bytes))
        prompt = request["prompt"]

        model_inputs = self.processor(
            text=prompt, images=image, return_tensors="pt"
        ).to(self.model.device)
        return model_inputs

    def predict(self, model_inputs):
        input_len = model_inputs["input_ids"].shape[-1]
        with torch.inference_mode():
            generation = self.model.generate(
                **model_inputs, max_new_tokens=100, do_sample=False
            )
            generation = generation[0][input_len:]
            decoded = self.processor.decode(generation, skip_special_tokens=True)
            return decoded

    def encode_response(self, output):
        # Convert the model output to a response payload.
        return {"output": output}


if __name__ == "__main__":
    api = PaliGemmaLitAPI()
    server = ls.LitServer(api)
    server.run(port=8000)
