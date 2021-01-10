from flask import request
from app import app
from basic.database import db
from basic.models import *
from dateutil.parser import parse as date_parse
from basic.util import token_required, create_response


@app.route('/meals/', methods=['GET'])
@token_required
def get_meals(current_user):
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    return create_response({'meals': [meal.data() for meal in meals]}, 200, '*')


@app.route('/meals/', methods=['POST'])
@token_required
def create_meal(current_user):
    data = request.get_json()

    try:
        name = data['name']
    except:
        name = None
    try:
        date = date_parse(data['date'])
    except:
        date = None

    new_meal = Meal(name=name, date=date, user_id=current_user.id)
    db.session.add(new_meal)
    db.session.commit()

    return create_response({'message': 'Meal created!', 'id': new_meal.id}, 200, '*')


@app.route('/meals/<int:meal_id>', methods=['GET'])
@token_required
def get_meal(current_user, meal_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal == None:
        return create_response({'message': 'Meal not found!'}, 404, '*')

    return create_response(meal.data(), 200, '*')


@app.route('/meals/<int:meal_id>', methods=['PUT'])
@token_required
def modify_meal(current_user, meal_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal == None:
        return create_response({'message': 'Meal not found!'}, 404, '*')

    data = request.get_json()

    if 'name' in data.keys():
        meal.name = data['name']
    if 'date' in data.keys():
        meal.date = date_parse(data['date'])

    db.session.commit()

    return create_response({'message': 'Meal updated!'}, 200, '*')


@app.route('/meals/<int:meal_id>', methods=['DELETE'])
@token_required
def delete_meal(current_user, meal_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal == None:
        return create_response({'message': 'Meal not found!'}, 404, '*')

    # Clean out associated foods
    foods = Food.query.filter_by(meal_id=meal.id).all()
    for food in foods:
        db.session.delete(food)

    db.session.delete(meal)
    db.session.commit()

    return create_response({'message': 'Meal deleted!'}, 200, '*')
