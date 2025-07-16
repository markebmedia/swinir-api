from flask import Flask, request, jsonify
from PIL import Image
import io
import traceback

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({ "message": "SwinIR API is live 🚀" })

@app.route("/enhance", methods=["POST"])
def enhance():
    try:
        image_file = request.files['image']
        print("📸 Received file:", image_file.filename)

        # Validate the image using PIL
        image = Image.open(image_file.stream)
        image.verify()  # Ensure it's a valid image
        print("✅ Image verified")

        # Simulate enhancement and return a dummy URL
        enhanced_url = "https://dummy-markeb.s3.amazonaws.com/enhanced.jpg"
        return jsonify({ "enhanced_url": enhanced_url })

    except Exception as e:
        print("🔥 Enhancement failed:", e)
        traceback.print_exc()
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
