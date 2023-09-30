#!/usr/bin/python3
"""Starts a Flask web application.
"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv


host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(eception):
    storage.close()


@app.errorhandler(404)
def show_404(exception):
    return jsonify({
        "error": "Not found"
    })


if __name__ == "__main__":
    if port is None:
        port = 5000
    if host is None:
        host = "0.0.0.0"

    app.run(host=host, port=port, threaded=True)
