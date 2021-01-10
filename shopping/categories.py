from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response


@app.route('/categories/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return create_response({'categories': [category.data() for category in categories]}, 200, '*')


@app.route('/categories/<string:category>/tags/', methods=['GET'])
def get_category_tags(category):
    try:
        category = Category.query.filter_by(title=category).first()
        if not category:
            return create_response({'message': 'Category not found!'}, 404, '*')

        tags = []
        for product in category.products:
            for tag in product.tags:
                data = tag.data()
                if data not in tags:
                    tags.append(data)

        return create_response({'tags': tags}, 200, '*')
    except Exception as e:
        return create_response({'message': str(e)}, 200, '*')


@app.route('/categories/<string:category>', methods=['POST'])
@token_required
def create_category(current_user, category):
    if not current_user.admin:
        return create_response({'message': 'Cannot perform that function!'}, 401)

    existing = Category.query.filter_by(title=category).first()
    if existing:
        create_response({'message': 'Category already exists!'}, 401)
    else:
        new = Category(title=category)
        db.session.add(new)
        db.session.commit()

    return create_response({'message': 'Category Created!'}, 200, '*')


@app.route('/categories/<string:category>', methods=['DELETE'])
@token_required
def delete_category(current_user, category):
    if not current_user.admin:
        return create_response({'message': 'Cannot perform that function!'}, 401)

    existing = Category.query.filter_by(title=category).first()
    if not existing:
        return create_response({'message': 'Category not found!'}, 404, '*')

    db.session.delete(existing)
    db.session.commit()
    return create_response({'message': 'Category Deleted!'}, 200, '*')
