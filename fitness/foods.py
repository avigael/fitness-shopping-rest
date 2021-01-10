from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response


@app.route('/meals/<int:meal_id>/foods/', methods=['GET'])
@token_required
def get_foods(current_user, meal_id):
    meal_data = Meal.query.filter_by(
        user_id=current_user.id, id=meal_id).first()

    if meal_data == None:
        return create_response({'message': 'Meal not found!'}, 404, '*')

    foods = Food.query.filter_by(meal_id=meal_data.id).all()

    return create_response({'foods': [food.data() for food in foods]}, 200, '*')


@app.route('/meals/<int:meal_id>/foods/', methods=['POST'])
@token_required
def create_food(current_user, meal_id):
    try:
        data = request.get_json()

        meal = Meal.query.filter_by(
            user_id=current_user.id, id=meal_id).first()

        if meal == None:
            return create_response({'message': 'Meal not found!'}, 404, '*')

        if data:
            name = data.get('name', None)
            calories = data.get('calories', None)
            carbohydrates = data.get('carbohydrates', None)
            protein = data.get('protein', None)
            fat = data.get('fat', None)
        else:
            return create_response({'message': 'No data provided'}, 400, '*')

        new_food = Food(meal_id=meal.id, name=name, calories=calories,
                        protein=protein, carbohydrates=carbohydrates, fat=fat)

        db.session.add(new_food)
        db.session.commit()
        return create_response({'message': 'Food created!', 'id': new_food.id}, 200, '*')
    except Exception as e:
        return create_response({'message': str(e)}, 500, '*')


@app.route('/meals/<int:meal_id>/foods/<int:food_id>', methods=['GET'])
@token_required
def get_food(current_user, meal_id, food_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal == None:
        return create_response({'message': 'Meal not found!'}, 404, '*')

    food = Food.query.filter_by(meal_id=meal.id, id=food_id).first()

    if food == None:
        return create_response({'message': 'Food not found!'}, 404, '*')

    return create_response(food.data(), 200, '*')


@app.route('/meals/<int:meal_id>/foods/<int:food_id>', methods=['PUT'])
@token_required
def modify_food(current_user, meal_id, food_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal == None:
        return create_response({'message': 'Meal not found!'}, 404, '*')

    food = Food.query.filter_by(meal_id=meal.id, id=food_id).first()

    if food == None:
        return create_response({'message': 'Food not found!'}, 404, '*')

    data = request.get_json()
    for key in data.keys():
        if key == 'name':
            food.name = data['name']
        elif key == 'calories':
            food.calories = data['calories']
        elif key == 'protein':
            food.protein = data['protein']
        elif key == 'carbohydrates':
            food.carbohydrates = data['carbohydrates']
        elif key == 'fat':
            food.fat = data['fat']

    db.session.commit()
    return create_response({'message': 'Food updated!'}, 200, '*')


@app.route('/meals/<int:meal_id>/foods/<int:food_id>', methods=['DELETE'])
@token_required
def delete_food(current_user, meal_id, food_id):
    meal = Meal.query.filter_by(user_id=current_user.id, id=meal_id).first()

    if meal == None:
        return create_response({'message': 'Meal not found!'}, 404, '*')

    food = Food.query.filter_by(meal_id=meal.id, id=food_id).first()

    if food == None:
        return create_response({'message': 'Food not found!'}, 404, '*')

    db.session.delete(food)
    db.session.commit()

    return create_response({'message': 'Food deleted!'}, 200, '*')
