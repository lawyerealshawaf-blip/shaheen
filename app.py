import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

# تحميل متغيرات البيئة محلياً فقط
load_dotenv()

app = Flask(__name__)

# إعداد العميل داخل دالة أو التأكد من وجود المفتاح لمنع انهيار التشغيل
def get_ai_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    client = get_ai_client()
    
    if not client:
        return jsonify({"error": "API Key is missing on Vercel settings"}), 500
        
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=user_input
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# مهم جداً لـ Vercel
app.debug = False
