from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import requests as axios
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def check():
    return("Working fine ok ")
    

@app.route('/do')
def do_this():
    # return("hello")
    try:
        response = axios.get("https://669f704cb132e2c136fdd9a0.mockapi.io/api/v1/retreats")
        retreatList = response.json()

        for retreat in retreatList:
            axios.post("http://127.0.0.1:5000/retreat", json=retreat)
        return "Updated the table", 200
    
    except Exception as e:
        return jsonify({"Error": e}), 400
    


if __name__ == "__main__":
    # app = create_app()
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)