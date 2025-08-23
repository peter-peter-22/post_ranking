import torch

# Get device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
