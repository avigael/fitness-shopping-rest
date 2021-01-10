from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/users/', methods=['GET'])
@token_required
def get_users(current_user):

    if not current_user.admin:
        return create_response({'message': 'Cannot perform that function!'}, 401)

    users = User.query.all()

    return create_response({'users': [user.data() for user in users]}, 200, '*')


@app.route('/users/<string:username>', methods=['GET'])
@token_required
def get_user(current_user, username):
    if current_user.username != username and not current_user.admin:
        return create_response({'message': 'Incorrect user'}, 401, '*')

    user = User.query.filter_by(username=username).first()
    if not user:
        return create_response({'message': 'User not found!'}, 404, '*')

    return create_response(user.data(), 200, '*')


@app.route('/users/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        if not data:
            return create_response({'message': 'No data provided!'}, 400, '*')

        print(data)

        missing = []
        for field in ['username', 'password']:
            if field not in data.keys():
                missing.append(field)
            elif data[field] == None or len(str(data[field])) < 5:
                return create_response({'message': 'Field {0} must be 5 characters or longer.'.format(field)}, 400, '*')
        if len(missing) > 0:
            return create_response({'message': 'Missing required fields: '+', '.join(missing)}, 400, '*')

        user = User.query.filter_by(username=data['username']).first()

        if user:
            return create_response({'message': 'Username already taken!'}, 409, '*')

        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        user = User(username=data['username'],
                    password=hashed_password,
                    first_name=data.get('firstName', None),
                    last_name=data.get('lastName', None),
                    goal_daily_calories=data.get('goalDailyCalories', None),
                    goal_daily_carbohydrates=data.get(
                        'goalDailyCarbohydrates', None),
                    goal_daily_protein=data.get('goalDailyProtein', None),
                    goal_daily_fat=data.get('goalDailyFat', None),
                    goal_daily_activity=data.get('goalDailyActivity', None),
                    admin=False)

        user.application = Application()

        db.session.add(user)
        db.session.commit()
        return create_response({'message': 'User created!'}, 200, '*')
    except Exception as e:
        return create_response({'message': str(e)}, 500, '*')


@app.route('/users/<string:username>', methods=['PUT'])
@token_required
def modify_user(current_user, username):
    if current_user.username != username and not current_user.admin:
        return create_response({'message': 'Incorrect User'}, 401, '*')

    user = User.query.filter_by(username=username).first()
    if not user:
        return create_response({'message': 'User not found!'}, 404, '*')

    data = request.get_json()

    for key in data.keys():
        if key == 'firstName':
            user.first_name = data['firstName']
        elif key == 'lastName':
            user.last_name = data['lastName']
        elif key == 'password':
            user.password = generate_password_hash(
                data['password'], method='sha256')
        elif key == 'goalDailyCalories':
            user.goal_daily_calories = data['goalDailyCalories']
        elif key == 'goalDailyProtein':
            user.goal_daily_protein = data['goalDailyProtein']
        elif key == 'goalDailyCarbohydrates':
            user.goal_daily_carbohydrates = data['goalDailyCarbohydrates']
        elif key == 'goalDailyFat':
            user.goal_daily_fat = data['goalDailyFat']
        elif key == 'goalDailyActivity':
            user.goal_daily_activity = data['goalDailyActivity']
        elif key == 'admin' and current_user.admin:
            user.admin = data['admin']

    db.session.commit()
    return ({'message': 'User has been updated!'}, 200)


@app.route('/users/<string:username>', methods=['DELETE'])
@token_required
def delete_user(current_user, username):
    if current_user.username != username and not current_user.admin:
        return create_response({'message': 'Incorrect User'}, 401, '*')

    user = User.query.filter_by(username=username).first()
    if not user:
        return create_response({'message': 'User not found!'}, 404, '*')

    # Remove associated meals, foods, and activities
    meals = Meal.query.filter_by(user_id=current_user.id).all()
    for meal in meals:
        foods = Food.query.filter_by(meal_id=meal.id).all()
        for food in foods:
            db.session.delete(food)
        db.session.delete(meal)
    activities = Activity.query.filter_by(user_id=current_user.id).all()
    for activity in activities:
        db.session.delete(activity)
    for assoc in user.application.cart:
        db.session.delete(assoc)
    db.session.delete(user.application)
    db.session.delete(user)
    db.session.commit()

    return create_response({'message': 'User has been deleted!'}, 200, '*')


@app.route('/login/')
def login():
    auth = request.authorization

    if not auth:
        return create_response({'message': 'No auth found!'}, 401, '*', True)
    elif not auth.username or not auth.password:
        return create_response({'message': '"username" and/or "password" not found in auth'}, 401, '*', True)

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return create_response({'message': 'Could not verify'}, 401, True, '*')

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return create_response({'token': token.decode('UTF-8')}, 200, '*')

    return create_response({'message': 'Could not verify'}, 401, '*', True)
