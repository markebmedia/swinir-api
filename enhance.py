from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import os
import uuid
import traceback
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError

from swinir_enhancer import enhance_with_swinir

# Load .env
load_dotenv()

app = Flask(__name__)

# Constants
OUTPUT_FOLDER = os.path.join(os.getcwd(), "outputs")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5050")

# S3 uploader
def upload_to_s3(file_path, filename):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        s3.upload_file(file_path, S3_BUCKET, filename, ExtraArgs={'ACL': 'public-read'})
        url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"
        return url
    except NoCredentialsError:
        print("❌ AWS credentials missing.")
        return None
    except Exception as e:
        print("❌ S3 upload failed:", e)
        return None

# Health check
@app.route("/", methods=["GET"])
def home():
    return jsonify({ "message": "SwinIR API is live 🚀" })

# Enhance route
@app.route("/enhance", methods=["POST"])
def enhance():
    try:
        image_file = request.files['image']
        print("📸 Received file:", image_file.filename)

        # Save uploaded file temporarily
        raw_filename = f"input_{uuid.uuid4()}.jpg"
        input_path = os.path.join(OUTPUT_FOLDER, raw_filename)
        image_file.save(input_path)

        # Define output path
        output_filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Run SwinIR enhancement
        print("🧠 Enhancing image with SwinIR...")
        enhance_with_swinir(input_path, output_path)

        # Upload to S3
        print("☁️ Uploading enhanced image to S3...")
        s3_url = upload_to_s3(output_path, output_filename)

        if s3_url:
            print("✅ Done. Enhanced image URL:", s3_url)
            return jsonify({ "enhanced_url": s3_url })
        else:
            fallback_url = f"{BASE_URL}/outputs/{output_filename}"
            print("⚠️ S3 failed. Returning local URL:", fallback_url)
            return jsonify({ "enhanced_url": fallback_url })

    except Exception as e:
        print("🔥 Enhancement failed:", e)
        traceback.print_exc()
        return jsonify({ "error": str(e) }), 500

# Serve local outputs for dev
@app.route("/outputs/<filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)

