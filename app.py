from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "نظام شاهين الذكي يعمل بنجاح"

if __name__ == "__main__":
    app.run()
