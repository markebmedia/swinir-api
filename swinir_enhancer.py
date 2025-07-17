# swinir_enhancer.py
import sys
import os

# Dynamically add BasicSR folder to Python path (works on Render + locally)
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(base_dir, 'BasicSR'))

import torch
import numpy as np
import cv2
from basicsr.archs.swinir_arch import SwinIR

# Absolute path to your pretrained model (relative to this script)
model_path = os.path.join(base_dir, "experiments", "pretrained_models", "SwinIR_model.pth")

# Load SwinIR model
def load_model():
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ SwinIR model not found at: {model_path}")

    print("📦 Loading SwinIR model...")
    model = SwinIR(
        upscale=4,  # Use 1 if you don't want super-resolution
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
    print("✅ SwinIR model loaded successfully")
    return model

# Enhance image with SwinIR
def enhance_with_swinir(input_path, output_path):
    print(f"🖼️ Enhancing image: {input_path}")
    try:
        # Load image using OpenCV (BGR)
        img = cv2.imread(input_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("❌ Failed to read image. Make sure the path is correct.")

        img = img.astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(np.transpose(img, (2, 0, 1))).float().unsqueeze(0)  # CHW -> BCHW

        # Load model
        model = load_model()

        with torch.no_grad():
            output_tensor = model(img_tensor)

        # Convert output tensor to image
        output_img = output_tensor.squeeze().clamp(0, 1).cpu().numpy()
        output_img = (np.transpose(output_img, (1, 2, 0)) * 255.0).round().astype(np.uint8)
        output_img = cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV

        cv2.imwrite(output_path, output_img)
        print(f"✅ Enhanced image saved to: {output_path}")

    except Exception as e:
        print("🔥 Enhancement failed:", e)
        raise e

