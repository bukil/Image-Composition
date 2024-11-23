from flask import Flask, request, render_template, jsonify
from PIL import Image
import io
import os
import openai

# Initialize Flask app
app = Flask(__name__)

# Set NeVA API Key
# associated with mukilk@iitb.ac.in
openai.api_key = "nvami-xTr1qKfrG8ucv9zjxB4DD5R1eJOA77udvXlOBW4nATMy8W_rkHRETnX5RhUqcIwp"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]

    # Ensure file is an image
    try:
        image = Image.open(file.stream)
    except IOError:
        return jsonify({"error": "Invalid image file"}), 400

    # Convert image to a byte stream (if further AI processing needed)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()

    # Example: AI model generates a description (use OpenAI here)
    response = openai.ChatCompletion.create(
        model="neva-22b preview",
        messages=[
            {
                "role": "system",
                "content": "Prado biases"
            },
            {
                "role": "user",
                "content": "Mukil_IDC_or_IXD_Biases."
            }
        ]
    )

    # Get explanation text
    explanation = response["choices"][0]["message"]["content"]

    return jsonify({"explanation": explanation})

if __name__ == "__main__":
    app.run(debug=True)
