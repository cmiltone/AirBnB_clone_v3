#!/usr/bin/python3
"""
module creates review route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'], strict_slashes=False)
def reviews():
    """reviews route"""
    if request.method == 'GET':
        _reviews = storage.all('Review')
        reviews_list = []
        for review in _reviews.values():
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if json.get('name') is None:
            abort(400, 'Missing name')
        if json.get('text') is None:
            abort(400, 'Missing text')
        obj = Review(**json)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_id(review_id=None):
    """review with id route"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(obj.to_dict())

    if request.method == 'DELETE':
        obj.delete()
        del obj
        return jsonify({}), 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        obj.update(json)
        return jsonify(obj.to_dict()), 200
