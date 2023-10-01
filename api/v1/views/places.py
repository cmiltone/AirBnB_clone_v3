#!/usr/bin/python3
"""
module creates place route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City

from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def places(city_id=None):
    """places route"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        all_places = storage.all('Place')
        places_list = []
        for state in all_places.values():
            places_list.append(state.to_dict())
        return jsonify(places_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if json.get('name') is None:
            abort(400, 'Missing name')
        json['city_id'] = city_id
        obj = Place(**json)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_id(place_id=None):
    """state with id route"""
    obj = storage.get(Place, place_id)
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
