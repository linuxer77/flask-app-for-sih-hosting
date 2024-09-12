from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://tourism-and-travel-sih.vercel.app"}})
from app import routes
if __name__ == '__main__':
    app.run(debug=True)

