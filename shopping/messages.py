from flask import request
from app import app
from basic.database import db
from basic.models import *
from dateutil.parser import parse as date_parse
from basic.util import token_required, create_response


@app.route('/application/messages/', methods=['GET'])
@token_required
def get_application_messages(current_user):
    if not current_user.application:
        current_user.application = Application()

    messages = [message.data()
                for message in current_user.application.messages]
    return create_response({'messages': messages}, 200, '*')


@app.route('/application/messages/', methods=['DELETE'])
@token_required
def delete_application_messages(current_user):
    if not current_user.application:
        current_user.application = Application()

    for message in current_user.application.messages:
        db.session.delete(message)

    current_user.application.messages = []
    db.session.commit()
    return create_response({'messages': 'All messages removed from application state!'}, 200, '*')


@app.route('/application/messages/<int:message_id>', methods=['GET'])
@token_required
def get_application_message(current_user, message_id):
    if not current_user.application:
        current_user.application = Application()

    messages = [
        message for message in current_user.application.messages if message.id == message_id]
    if len(messages) < 1:
        return create_response({'message': 'Message not found!'}, 404, '*')

    return create_response(messages[0].data(), 200, '*')


@app.route('/application/messages/', methods=['POST'])
@token_required
def create_application_message(current_user):
    if not current_user.application:
        current_user.application = Application()

    data = request.get_json()

    try:
        date = date_parse(data['date'])
    except:
        date = None

    new_message = Message(date=date,
                          application_id=current_user.application.id,
                          is_user=data.get('isUser', None),
                          text=data.get('text', None))
    db.session.add(new_message)
    current_user.application.messages.append(new_message)
    db.session.commit()
    return create_response({'message': 'Message created!', 'id': new_message.id}, 200, '*')


@app.route('/application/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_application_message(current_user, message_id):
    if not current_user.application:
        current_user.application = Application()

    existing_message = Message.query.filter_by(id=message_id).first()
    if not existing_message:
        return create_response({'message': 'Message not found!'}, 404, '*')

    db.session.delete(existing_message)
    current_user.application.messages = [
        message for message in current_user.application.messages if message.id != message_id]
    db.session.commit()

    return create_response({'message': 'Message deleted!'}, 200, '*')
