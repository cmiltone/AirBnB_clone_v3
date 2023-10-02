#!/usr/bin/python3
"""
module creates place route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.amenity import Amenity
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def places(city_id=None):
    """places route"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        all_places = storage.all(Place)
        places_list = []
        for state in all_places.values():
            places_list.append(state.to_dict())
        return jsonify(places_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if json.get('user_id') is None:
            abort(400, 'Missing user_id')
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


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """places search route"""
    all_places = [p for p in storage.all(Place).values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all(City)
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get(City, c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get(Amenity, a_id)])
        for p in all_places:
            p_amenities = None
            if storage_t == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
