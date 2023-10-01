#!/usr/bin/python3
"""
module creates city route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def cities():
    """cities route"""
    all_cities = storage.all(City)
    cities_list = []
    for city in all_cities.values():
        cities_list.append(city.to_dict())
    return jsonify(cities_list)

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def states_cities(state_id=None):
    """create cities route"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        all_cities = storage.all(City)
        cities = []
        for city in all_cities:
            if city.get('state_id') == state_id:
                cities.append(city.to_dict())
        return jsonify(cities), 200
    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if json.get('name') is None:
            abort(400, 'Missing name')
        json['state_id'] = state_id
        obj = City(**json)
        obj.save()
        return jsonify(obj.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_id(city_id=None):
    """city with id route"""
    obj = storage.get(City, city_id)
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
