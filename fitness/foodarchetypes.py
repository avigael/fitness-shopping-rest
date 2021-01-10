from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response


@app.route('/foods/', methods=['GET'])
def get_food_archetypes():

    foods = FoodArchetype.query.all()

    return create_response({'foods': [food.data() for food in foods]}, 200, '*')


@app.route('/foods/<int:food_id>', methods=['GET'])
def get_food_archetype(food_id):
    food = FoodArchetype.query.filter_by(id=food_id).first()

    if food:
        return create_response(food.data(), 200, '*')
    else:
        return create_response({'message': 'Food not found!'}, 404, '*')


@app.route('/foods/', methods=['POST'])
@token_required
def create_food_archetype(current_user):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    data = request.get_json()

    if data == None:
        return create_response({'message': 'No data provided!'}, 400, '*')

    name = data.get('name', None)
    measure = data.get('measure', None)
    calories = data.get('calories', None)
    protein = data.get('protein', None)
    carbohydrates = data.get('carbohydrates', None)
    fat = data.get('fat', None)

    new_food = FoodArchetype(name=name,
                             measure=measure,
                             calories=calories,
                             protein=protein,
                             carbohydrates=carbohydrates,
                             fat=fat)

    db.session.add(new_food)
    db.session.commit()
    return create_response({'message': 'Food created!', 'id': new_food.id}, 200, '*')


@app.route('/foods/', methods=['PUT'])
@token_required
def modify_food_archetypes(current_user):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    data = request.get_json()

    if data == None:
        return create_response({'message': 'No data provided!'}, 400, '*')

    for food in FoodArchetype.query.all():
        db.session.delete(food)

    for food in data.get('foods', []):
        new_food = FoodArchetype(name=food.get('name', None),
                                 measure=food.get('measure', None),
                                 calories=food.get('calories', None),
                                 protein=food.get('protein', None),
                                 carbohydrates=food.get('carbohydrates', None),
                                 fat=food.get('fat', None))

        db.session.add(new_food)
    db.session.commit()

    return create_response({'message': 'Foods modified!'}, 200, '*')


@app.route('/foods/<int:food_id>', methods=['PUT'])
@token_required
def modify_food_archetype(current_user, food_id):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    data = request.get_json()

    if not data:
        return create_response({'message': 'No data provided!'}, 400, '*')

    food = FoodArchetype.query.filter_by(id=food_id).first()

    if not food:
        return create_response({'message': 'Food not found!'}, 404, '*')

    if 'name' in data.keys():
        food.name = data['name']
    if 'measure' in data.keys():
        food.measure = data['measure']
    if 'calories' in data.keys():
        food.calories = data['calories']
    if 'protein' in data.keys():
        food.protein = data['protein']
    if 'carbohydrates' in data.keys():
        food.carbohydrates = data['carbohydrates']
    if 'fat' in data.keys():
        food.fat = data['fat']

    db.session.commit()
    return create_response({'message': 'Food updated!'}, 200, '*')


@app.route('/foods/<int:food_id>', methods=['DELETE'])
@token_required
def delete_food_archetype(current_user, food_id):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    food = FoodArchetype.query.filter_by(id=food_id).first()

    if not food:
        return create_response({'message': 'Food not found!'}, 404, '*')

    db.session.delete(food)
    db.session.commit()

    return create_response({'message': 'Food deleted!'}, 200, '*')
