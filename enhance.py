from flask import Flask, request, jsonify

app = Flask(__name__)

# Root route for health check
@app.route("/", methods=["GET"])
def home():
    return jsonify({ "message": "SwinIR API is live 🚀" })

# POST route for image enhancement (to be expanded)
@app.route("/enhance", methods=["POST"])
def enhance():
    # Placeholder logic
    return jsonify({ "status": "success", "message": "Enhancement endpoint is ready" })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

