from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response


@app.route('/application', methods=['GET'])
@token_required
def get_application(current_user):
    return create_response(current_user.application.data(), 200, '*')


@app.route('/application', methods=['PUT'])
@token_required
def modify_application(current_user):
    if not current_user.application:
        current_user.application = Application()

    data = request.get_json()

    if 'page' in data.keys():
        current_user.application.page = data['page']
    if 'back' in data.keys():
        current_user.application.back = data['back']
    if 'dialogflowUpdated' in data.keys():
        current_user.application.dialogflow_updated = data['dialogflowUpdated']
    else:
        current_user.application.dialogflow_updated = True

    db.session.commit()

    return create_response({'message': 'Application state modified!'}, 200, '*')


@app.route('/application/tags/', methods=['GET'])
@token_required
def get_application_tags(current_user):
    if not current_user.application:
        current_user.application = Application()

    return create_response({'tags': [tag.data() for tag in current_user.application.tags]}, 200, '*')


@app.route('/application/tags/', methods=['DELETE'])
@token_required
def delete_application_tags(current_user):
    if not current_user.application:
        current_user.application = Application()

    try:
        current_user.application.tags = []
        db.session.commit()
    except Exception as e:
        return create_response({'message': st(e)}, 500)

    return create_response({'message': 'All tags removed from application state!'}, 200, '*')


@app.route('/application/tags/<string:tag>', methods=['POST'])
@token_required
def create_application_tag(current_user, tag):
    if not current_user.application:
        current_user.application = Application()

    existing_tag = Tag.query.filter_by(value=tag).first()
    if not existing_tag:
        return create_response({'message': 'Tag not found!'}, 404, '*')

    current_user.application.tags.append(existing_tag)
    db.session.commit()

    return create_response({'message': 'Tag added to application state!'}, 200, '*')


@app.route('/application/tags/<string:tag>', methods=['DELETE'])
@token_required
def delete_application_tag(current_user, tag):
    if not current_user.application:
        current_user.application = Application()

    existing_tag = Tag.query.filter_by(value=tag).first()
    if not existing_tag:
        return create_response({'message': 'Tag not found!'}, 404, '*')

    current_user.application.tags.remove(existing_tag)
    db.session.commit()

    return create_response({'message': 'Tag removed from application state!'}, 200, '*')


@app.route('/application/products/', methods=['GET'])
@token_required
def get_application_products(current_user):
    if not current_user.application:
        current_user.application = Application()

    data = []
    for cart_assoc in current_user.application.cart:
        product_data = cart_assoc.product.data()
        product_data['count'] = cart_assoc.count
        data.append(product_data)

    return create_response({'products': data}, 200, '*')


@app.route('/application/products/<int:product_id>', methods=['GET'])
@token_required
def get_application_product(current_user, product_id):
    if not current_user.application:
        current_user.application = Application()

    cart_assocs = [
        assoc for assoc in current_user.application.cart if assoc.product.id == product_id]

    if len(cart_assocs) < 1:
        return create_response({'message': 'Product not found!'}, 404, '*')

    data = cart_assocs[0].product.data()
    data['count'] = cart_assocs[0].count
    return create_response(data, 200, '*')


@app.route('/application/products/<int:product_id>', methods=['POST'])
@token_required
def create_application_product(current_user, product_id):
    if not current_user.application:
        current_user.application = Application()

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    cart_assocs = [
        assoc for assoc in current_user.application.cart if assoc.product.id == product_id]

    if len(cart_assocs) < 1:
        new_assoc = Cart(application_id=current_user.application.id,
                         product_id=product.id,
                         count=1)
        current_user.application.cart.append(new_assoc)
        db.session.add(new_assoc)
    else:
        cart_assocs[0].count += 1

    db.session.commit()

    return create_response({'message': 'Product added to cart!'}, 200, '*')


@app.route('/application/products/', methods=['DELETE'])
@token_required
def clear_application_products(current_user):
    if not current_user.application:
        current_user.application = Application()

    for assoc in current_user.application.cart:
        db.session.delete(assoc)
    db.session.commit()

    return create_response({'message': 'Cart cleared!'}, 200, '*')


@app.route('/application/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_application_product(current_user, product_id):
    try:
        if not current_user.application:
            current_user.application = Application()

        cart_assocs = [
            assoc for assoc in current_user.application.cart if assoc.product.id == product_id]

        if len(cart_assocs) < 1:
            return create_response({'message': 'Product not found!'}, 404, '*')

        if cart_assocs[0].count > 1:
            cart_assocs[0].count -= 1
        else:
            db.session.delete(cart_assocs[0])

        #current_user.application.cart = cart_assocs

        db.session.commit()

        return create_response({'message': 'Product removed from cart!'}, 200, '*')
    except Exception as e:
        return create_response({'message': str(e)}, 500, '*')
