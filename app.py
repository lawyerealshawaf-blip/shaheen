import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_ai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")

    client = get_ai_client()
    if not client:
        return jsonify({"error": "API Key is missing"}), 500

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# لضمان التوافق مع Vercel
app.debug = False

if __name__ == "__main__":
    app.run()
