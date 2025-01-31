#!/usr/bin/python3
"""
module creates state route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """states route"""
    if request.method == 'GET':
        _states = storage.all('State')
        states_list = []
        for state in _states.values():
            states_list.append(state.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if json.get('name') is None:
            abort(400, 'Missing name')
        obj = State(**json)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_id(state_id=None):
    """state with id route"""
    obj = storage.get(State, state_id)
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
