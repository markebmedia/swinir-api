# swinir_enhancer.py
import sys
import os

# Add cloned BasicSR folder to Python path to resolve imports
sys.path.append(os.path.join(os.getcwd(), 'BasicSR'))

import torch
import numpy as np
import cv2
from basicsr.archs.swinir_arch import SwinIR

# Path to your pretrained model (adjust if needed)
model_path = "experiments/pretrained_models/SwinIR_model.pth"

def load_model():
    model = SwinIR(
        upscale=4,
        in_chans=3,
        img_size=64,
        window_size=8,
        img_range=1.0,
        depths=[6, 6, 6, 6, 6, 6],
        embed_dim=180,
        num_heads=[6, 6, 6, 6, 6, 6],
        mlp_ratio=2,
        upsampler='nearest+conv',
        resi_connection='1conv'
    )
    pretrained = torch.load(model_path, map_location='cpu')
    model.load_state_dict(pretrained['params'], strict=True)
    model.eval()
    return model

def enhance_with_swinir(input_path, output_path):
    # Load image using OpenCV (BGR)
    img = cv2.imread(input_path, cv2.IMREAD_COLOR).astype(np.float32) / 255.0
    # Convert to CHW and Tensor
    img = torch.from_numpy(np.transpose(img, (2, 0, 1))).float().unsqueeze(0)

    model = load_model()

    with torch.no_grad():
        output = model(img)

    # Convert tensor back to HWC image (RGB)
    output_img = output.squeeze().clamp(0, 1).cpu().numpy()
    output_img = (np.transpose(output_img, (1, 2, 0)) * 255.0).round().astype(np.uint8)
    # OpenCV uses BGR, convert RGB->BGR before saving
    output_img = cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR)

    cv2.imwrite(output_path, output_img)
