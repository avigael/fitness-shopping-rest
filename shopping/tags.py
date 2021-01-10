from flask import request
from app import app
from basic.database import db
from basic.models import *
from basic.util import token_required, create_response


@app.route('/tags/', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return create_response({'tags': [tag.data() for tag in tags]}, 200, '*')


@app.route('/tags/<string:tag>', methods=['POST'])
@token_required
def create_tag(current_user, tag):
    if not current_user.admin:
        return create_response({'message': 'Cannot perform that function!'}, 401)

    existing = Tag.query.filter_by(value=tag).first()
    if existing:
        create_response({'message': 'Tag already exists!'}, 401)
    else:
        new = Tag(value=tag)
        db.session.add(new)
        db.session.commit()

    return create_response({'message': 'Tag Created!'}, 200, '*')


@app.route('/tags/<string:tag>', methods=['DELETE'])
@token_required
def delete_tag(current_user, tag):
    if not current_user.admin:
        return create_response({'message': 'Cannot perform that function!'}, 401)

    existing = Tag.query.filter_by(value=tag).first()
    if not existing:
        return create_response({'message': 'Tag not found!'}, 404, '*')

    db.session.delete(existing)
    db.session.commit()
    return create_response({'message': 'Tag Deleted!'}, 200, '*')
