from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response


@app.route('/products/', methods=['GET'])
def get_products():

    args = {}
    category = request.args.get('category', None)
    tags = request.args.get('tags', "").split(",")
    if category:
        args['category_title'] = category
    products = Product.query.filter_by(**args).all()
    for tag in tags:
        if tag != '':
            products = [product for product in products if tag in [
                product_tag.value for product_tag in product.tags]]
    return create_response({'products': [product.data() for product in products]}, 200, '*')


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')
    return create_response(product.data(), 200, '*')


@app.route('/products/<int:product_id>/tags/', methods=['GET'])
def get_product_tags(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    return create_response({'tags': [tag.data() for tag in product.tags]}, 200, '*')


@app.route('/products/', methods=['POST'])
@token_required
def create_product(current_user):
    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    data = request.get_json()
    if not data:
        return create_response({'message': 'No data provided!'}, 400, '*')

    product = Product(name=data.get('name', None),
                      image=data.get('image', None),
                      price=data.get('price', None),
                      description=data.get('description', None)
                      )

    for review in data.get('reviews', []):
        review = Review(title=review.get('title', None),
                        stars=review.get('stars', None),
                        text=review.get('text', None))
        db.session.add(review)
        product.reviews.append(review)

    for tag in data.get('tags', []):
        added_tag = Tag.query.filter_by(value=tag).first()
        if not added_tag:
            added_tag = Tag(value=tag)
            db.session.add(added_tag)
        product.tags.append(added_tag)

    category_title = data.get('category', None)
    if category_title != None:
        category = Category.query.filter_by(title=category_title).first()
        if category == None:
            category = Category(title=category_title)
            db.session.add(category)
        product.category = category

    db.session.add(product)
    db.session.commit()

    return create_response({'message': 'Product created!', 'id': product.id}, 200, '*')


@app.route('/products/<int:product_id>', methods=['PUT'])
@token_required
def modify_product(current_user, product_id):
    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    data = request.get_json()
    if not data:
        return create_response({'message': 'No data provided!'}, 400, '*')

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    for key in data.keys():
        if key == 'name':
            product.name = data[key]
        elif key == 'image':
            product.image = data[key]
        elif key == 'price':
            product.price = data[key]
        elif key == 'description':
            product.description = data[key]
        elif key == 'category':
            category = Category.query.filter_by(title=data['category']).first()
            if category == None and data['category'] != None:
                category = Category(title=data['category'])
                db.session.add(category)
            product.category = category

    db.session.commit()

    return create_response({'message': 'Product updated!'}, 200, '*')


@app.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    db.session.delete(product)

    return create_response({'message': 'Product deleted!'}, 200, '*')


@app.route('/products/<int:product_id>/tags/<string:tag>', methods=['POST'])
@token_required
def create_product_tag(current_user, product_id, tag):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    # Check if tag exists:
    added_tag = Tag.query.filter_by(value=tag).first()
    if not added_tag:
        added_tag = Tag(value=tag)
        db.session.add(added_tag)

    product.tags.append(added_tag)
    db.session.commit()

    return create_response({'message': 'Tag added!'}, 200, '*')


@app.route('/products/<int:product_id>/tags/<string:tag>', methods=['DELETE'])
@token_required
def delete_product_tag(current_user, product_id, tag):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    # Check if tag exists:
    product.tags = [tag for tag in product.tags if tag.value != tag]
    db.session.commit()

    return create_response({'message': 'Tag added!'}, 200, '*')
