#!/usr/bin/python3
"""
module creates place amenities route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def list_place_amenities(place_id=None):
    """get amenities route"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')
    amenities_list = []
    for amenity in place.amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def place_amenities(place_id=None, amenity_id=None):
    """place amenities route"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, 'Not found')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, 'Not found')
    if request.method == 'POST':
        found = False
        if storage_t == 'db':
            for a in place.amenities:
                if a.id == amenity_id:
                    found = True
            if not found:
                place.amenities.append(amenity_id)
        else:
            for a in place.amenities:
                if a.id == amenity_id:
                    found = True
            if not found:
                place.amenity_ids.append(amenity_id)
        # obj = Place(**place.to_dict())
        place.save()
        status = 201
        if found:
            status = 200
        return jsonify(place.to_dict()), status

    if request.method == 'DELETE':
        found = False
        if storage_t == 'db':
            for i, a in enumerate(place.amenities):
                if a.id == amenity_id:
                    place.amenities.remove(i)
                    found = True
        else:
            for i, a in enumerate(place.amenities):
                if a.id == amenity_id:
                    place.amenity_ids.remove(i)
                    found = True
        if found:
            obj = Place(**place)
            obj.save()
        else:
            abort(404, 'Not found')
        return jsonify({}), 200
