#!/usr/bin/python3
"""Module for handling Review object RESTful API actions."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from datetime import datetime
import uuid


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
def list_reviews_of_place(place_id):
    ''' Retrieves the list of all Review objects of a Place. '''
    a_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in a_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    lsst_reviews = [obj.to_dict() for obj in storage.all("Review").values()
                    if place_id == obj.place_id]
    return jsonify(lsst_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    '''Retrieves a Review object.'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    a_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in a_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    a_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in a_users if obj.id == user_id]
    if user_obj == []:
        abort(404)
    reviews = []
    nss_review = Review(text=request.json['text'], place_id=place_id,
                        user_id=user_id)
    storage.new(nss_review)
    storage.save()
    reviews.append(nss_review.to_dict())
    return jsonify(reviews[0]), 201


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    '''Deletes a Review object. '''
    a_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in a_reviews if obj.id == review_id]
    if review_obj == []:
        abort(404)
    return jsonify(review_obj[0])


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    '''Deletes a Review object.'''
    a_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in a_reviews if obj.id == review_id]
    if review_obj == []:
        abort(404)
    review_obj.remove(review_obj[0])
    for obj in a_reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    '''updates a Review.'''
    a_reviews = storage.all("Review").values()
    review_obj = [obj.to_dict() for obj in a_reviews if obj.id == review_id]
    if review_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' in request.get_json():
        review_obj[0]['text'] = request.json['text']
        for obj in a_reviews:
            if obj.id == review_id:
                obj.text = request.json['text']
        storage.save()
    return jsonify(review_obj[0]), 200
