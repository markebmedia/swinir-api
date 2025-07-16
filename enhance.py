from flask import Flask, request, jsonify
from PIL import Image
import traceback
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({ "message": "SwinIR API is live 🚀" })

@app.route("/enhance", methods=["POST"])
def enhance():
    try:
        image_file = request.files['image']
        print("📸 Received file:", image_file.filename)

        image = Image.open(image_file.stream)
        image.verify()
        print("✅ Image verified")

        enhanced_url = "https://dummy-markeb.s3.amazonaws.com/enhanced.jpg"
        return jsonify({ "enhanced_url": enhanced_url })

    except Exception as e:
        print("🔥 Enhancement failed:", e)
        traceback.print_exc()
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    # ✅ Use PORT env if it exists (Render), otherwise default to 5050 locally
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)

