from flask import Flask, request, jsonify, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
import uuid
from werkzeug.security import generate_password_hash
from dateutil.parser import parse as date_parse
from dateutil.tz import gettz
import datetime

from app import app
from basic.database import db
from basic.models import *
from basic.tables import *
from basic.users import *
from basic.util import *
from fitness.activities import *
from fitness.foodarchetypes import *
from fitness.foods import *
from fitness.meals import *
from shopping.applications import *
from shopping.categories import *
from shopping.messages import *
from shopping.products import *
from shopping.reviews import *
from shopping.tags import *


tzinfo = gettz('America/Chicago')


def delete_empty_string_user():
    users = User.query.filter_by(username='').all()
    for user in users:
        db.session.delete(user)
    db.session.commit()


@app.route('/')
def index():
    return create_response({'message': 'Nothing here!'}, 200, '*')


if __name__ == '__main__':
    app.run(debug=False)
