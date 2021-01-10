from flask import request
from app import app
from basic.database import db
from basic.models import *
from dateutil.parser import parse as date_parse
from basic.util import token_required, create_response


@app.route('/activities/', methods=['GET'])
@token_required
def get_activities(current_user):
    activities = Activity.query.filter_by(user_id=current_user.id).all()

    return create_response({'activities': [activity.data() for activity in activities]}, 200, '*')


@app.route('/activities/', methods=['POST'])
@token_required
def create_activity(current_user):
    data = request.get_json()

    try:
        name = data['name']
    except:
        name = None
    try:
        duration = data['duration']
    except:
        duration = None
    try:
        date = date_parse(data['date'])
    except:
        date = None
    try:
        calories = data['calories']
    except:
        calories = None

    new_activity = Activity(name=name, duration=duration,
                            date=date, calories=calories, user_id=current_user.id)
    db.session.add(new_activity)
    db.session.commit()

    return create_response({'message': 'Activity created!', 'id': new_activity.id}, 200, '*')


@app.route('/activities/<int:activity_id>', methods=['GET'])
@token_required
def get_activity(current_user, activity_id):
    activity = Activity.query.filter_by(
        user_id=current_user.id, id=activity_id).first()

    if activity == None:
        return create_response({'message': 'Activity not found!'}, 404, '*')

    return create_response(activity.data(), 200, '*')


@app.route('/activities/<int:activity_id>', methods=['PUT'])
@token_required
def modify_activity(current_user, activity_id):
    activity = Activity.query.filter_by(
        user_id=current_user.id, id=activity_id).first()

    if activity == None:
        return create_response({'message': 'Activity not found!'}, 404, '*')

    data = request.get_json()

    if 'name' in data.keys():
        activity.name = data['name']
    if 'duration' in data.keys():
        activity.duration = data['duration']
    if 'date' in data.keys():
        activity.date = date_parse(data['date'])
    if 'calories' in data.keys():
        activity.calories = data['calories']

    db.session.commit()

    return create_response({'message': 'Activity updated!'}, 200, '*')


@app.route('/activities/<int:activity_id>', methods=['DELETE'])
@token_required
def delete_activity(current_user, activity_id):
    activity = Activity.query.filter_by(
        user_id=current_user.id, id=activity_id).first()

    if activity == None:
        return create_response({'message': 'Activity not found!'}, 404, '*')

    db.session.delete(activity)
    db.session.commit()

    return create_response({'message': 'Activity deleted!'}, 200, '*')
