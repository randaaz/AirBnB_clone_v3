#!/usr/bin/python3
"""Module to define API routes for managing states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/', methods=['GET'])
def l_states():
    '''Retrieves a list of all states.'''
    l_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(l_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def g_state(state_id):
    '''Retrieves details of a specific state.'''
    a_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in a_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    return jsonify(state_obj[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def d_state(state_id):
    '''Deletes a specific state.'''
    a_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in a_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    state_obj.remove(state_obj[0])
    for obj in a_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def c_state():
    '''Creates a new state.'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    n_state = State(name=request.json['name'])
    storage.new(n_state)
    storage.save()
    states.append(n_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def u_state(state_id):
    '''Updates details of a specific state.'''
    a_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in a_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in a_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
