#!/usr/bin/python3
"""
module creates user route
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """users route"""
    if request.method == 'GET':
        all_users = storage.all('User')
        users_list = []
        for state in all_users.values():
            users_list.append(state.to_dict())
        return jsonify(users_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, 'Not a JSON')
        if json.get('name') is None:
            abort(400, 'Missing name')
        obj = User(**json)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_id(user_id=None):
    """state with id route"""
    obj = storage.get(User, user_id)
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
