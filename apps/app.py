import os

from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    # Configuring MongoDB
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]
    mongo.init_app(app)

    # Adding blueprint
    from apps.url_shortener.controller import url_shortener
    app.register_blueprint(url_shortener)

    return app