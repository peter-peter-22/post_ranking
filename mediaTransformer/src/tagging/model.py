from src.common.device import device
from transformers.models.auto.processing_auto import AutoProcessor
import torch
from transformers.models.auto.modeling_auto import AutoModelForImageTextToText

# Get model and preprocessor
model_path = "HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
).to(device)

# Config preprocessor
processor.default_fps=0.5
processor.default_max_frames=10
