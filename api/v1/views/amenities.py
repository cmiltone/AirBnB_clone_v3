#!/usr/bin/python3
"""
module creates amenity route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """amenities route"""
    if request.method == 'GET':
        all_amenities = storage.all('Amenity')
        amenities_list = []
        for state in all_amenities.values():
            amenities_list.append(state.to_dict())
        return jsonify(amenities_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if json.get('name') is None:
            abort(400, 'Missing name')
        obj = Amenity(**json)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_id(state_id=None):
    """state with id route"""
    obj = storage.get(Amenity, state_id)
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
