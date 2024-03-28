#!/usr/bin/python3
"""Create a new view for Amenity"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid


@app_views.route('/amenities/', methods=['GET'])
def l_amenities():
    '''Retrieves a list of all amenities.'''
    l_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(l_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def g_amenity(amenity_id):
    '''Retrieves details of a specific amenity.'''
    a_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in a_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    return jsonify(amenity_obj[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def d_amenity(amenity_id):
    '''Deletes a specific amenity.'''
    a_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in a_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    amenity_obj.remove(amenity_obj[0])
    for obj in a_amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def c_amenity():
    '''Creates a new amenity.'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def u_amenity(amenity_id):
    '''Updates details of a specific amenity.'''
    a_amenities = storage.all("Amenity").values()
    amenity_obj = [obj.to_dict() for obj in a_amenities
                   if obj.id == amenity_id]
    if amenity_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_obj[0]['name'] = request.json['name']
    for obj in a_amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_obj[0]), 200
