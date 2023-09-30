#!/usr/bin/python3
"""
module creates status route
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def show_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def show_status():
    amenities = storage.count('Amenity')
    cities = storage.count('City')
    places = storage.count('Place')
    reviews = storage.count('Review')
    states = storage.count('State')
    users = storage.count('User')
    return jsonify({
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users
    })
