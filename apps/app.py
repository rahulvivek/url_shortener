import os

from flask import Flask
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)

    mongo = PyMongo()
    
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]

    mongo.init_app(app)


    @app.route("/health_check")
    def health_check():
        return "Ok"

    return app