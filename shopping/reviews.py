from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response


@app.route('/products/<int:product_id>/reviews/', methods=['GET'])
def get_product_reviews(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')
    return create_response({'reviews': [review.data() for review in product.reviews]}, 200, '*')


@app.route('/products/<int:product_id>/reviews/<int:review_id>', methods=['GET'])
def get_product_review(product_id, review_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    reviews = [review for review in product.reviews if review.id == review_id]
    if len(reviews) < 1:
        return create_response({'message': 'Review not found!'}, 404, '*')

    return create_response(reviews[0].data(), 200, '*')


@app.route('/products/<int:product_id>/reviews/', methods=['POST'])
@token_required
def create_product_review(current_user, product_id):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    data = request.get_json()

    try:
        date = data['date']
    except:
        date = None

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    title = db.Column(db.String(50), default='Review')
    stars = db.Column(db.Float(), default=2.5)
    text = db.Column(db.String(16000000), default='<Product Review Text>')

    review = Review(product_id=product.id,
                    title=data.get('title', None),
                    stars=data.get('stars', None),
                    text=data.get('text', None))

    db.session.add(review)
    product.reviews.append(review)
    db.session.commit()

    return create_response({'message': 'Review added!', 'id': review.id}, 200, '*')


@app.route('/products/<int:product_id>/reviews/<int:review_id>', methods=['PUT'])
@token_required
def modify_product_review(current_user, product_id, review_id):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    reviews = [review for review in product.reviews if review.id == review_id]
    if len(reviews) < 1:
        return create_response({'message': 'Review not found!'}, 404, '*')

    data = request.get_json()

    review = reviews[0]

    for key in data.keys():
        if key == 'title':
            review.title = data['title']
        elif key == 'stars':
            review.stars = data['stars']
        elif key == 'text':
            review.text = data['text']

    db.session.commit()

    return create_response({'message': 'Review updated!'}, 200, '*')


@app.route('/products/<int:product_id>/reviews/<int:review_id>', methods=['DELETE'])
@token_required
def delete_product_review(current_user, product_id, review_id):

    if not current_user.admin:
        return create_response({'message': 'Permission denied!'}, 403, '*')

    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return create_response({'message': 'Product not found!'}, 404, '*')

    product.reviews = [
        review for review in product.reviews if review.id != review_id]
    review = Product.query.filter_by(id=review_id).first()
    if review:
        db.session.delete(review)
    db.session.commit()

    return create_response({'message': 'Review deleted!'}, 200, '*')
