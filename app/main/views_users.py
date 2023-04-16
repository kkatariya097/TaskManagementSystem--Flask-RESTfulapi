from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required

from . import main
from .. import db
from ..models import Users, Tasks


@main.route('/users')
def get_users():
    sprints = Users.query.all()
    return jsonify({'success': True, 'data': sprints})


@main.route('/users/<int:user_id>')
@jwt_required()
def get_user_by_id(user_id):
    user = Users.query.get_or_404(user_id)
    return jsonify({'success': True, 'data': user})


@main.route('/users/<int:user_id>/tasks')
def get_tasks_by_user_id(user_id):
    tasks_by_user = Tasks.query.filter(Tasks.user_id == user_id).all()
    return jsonify({'success': True, 'data': tasks_by_user})


@main.route('/users', methods=['POST'])
@jwt_required(fresh=True)
def post_user():
    data = request.json
    user_id = data.get('user_id', None)
    if user_id:
        return {'success': False,
                'error': 'Should not have user id',
                'code': 409}, 409
    first_name = data.get('first_name', None)
    if not first_name:
        return {'success': False,
                'error': 'Missing first name',
                'code': 409}, 409
    last_name = data.get('last_name', None)
    if not last_name:
        return {'success': False,
                'error': 'Missing last name',
                'code': 409}, 409
    email = data.get('email', None)
    if not email:
        return {'success': False,
                'error': 'Missing email',
                'code': 409}, 409
    users = Users(user_id=user_id, first_name=first_name, last_name=last_name, email=email)
    db.session.add(users)
    db.session.commit()
    return jsonify({'success': True, 'data': users}, 200)


@main.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required(fresh=True)
def put_user(user_id):
    user = Users.query.get_or_404(user_id)
    data = request.json
    user_id = data.get('user_id', None)
    if user_id:
        return {'success': False,
                'error': 'Should not have user id to payload',
                'code': 408}, 408
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'data': user}, 200)


@main.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required(fresh=True)
def delete_user(user_id):
    result = db.session.execute(db.delete(Users).where(Users.user_id == user_id))
    db.session.commit()
    if result.rowcount == 1:
        return jsonify({'success': True, 'data': f'User {user_id} deleted'})
    else:
        abort(404)

