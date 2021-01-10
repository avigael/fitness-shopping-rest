from flask import make_response, jsonify, request
from app import app
import jwt
from basic.models import *
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return create_response({'message': 'Token is missing!'}, 401, '*')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        if not current_user:
            return create_response({'message': 'User does not exist!'}, 404, '*')

        return f(current_user, *args, **kwargs)

    return decorated


def create_response(data, code=200, origin='*', login_req=False):
    response = make_response(jsonify(data), code)
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Content-Type'] = 'json'
    response.headers['Vary'] = 'Origin'
    if login_req:
        response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return response
