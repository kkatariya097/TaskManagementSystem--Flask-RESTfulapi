from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required

from . import main
from .. import db
from ..models import Task_Status, Tasks, Sprints


@main.route('/tasks_status')
def get_status():
    status = Task_Status.query.all()
    return jsonify({'success': True, 'data': status})


@main.route('/tasks_status/<int:status_id>')
@jwt_required()
def get_status_by_id(status_id):
    user = Task_Status.query.get_or_404(status_id)
    return jsonify({'success': True, 'data': user})


@main.route('/tasks_status/<int:status_id>/tasks')
def get_tasks_by_status_id(status_id):
    tasks_by_status = Tasks.query.filter(Tasks.status_id == status_id).all()
    return jsonify({'success': True, 'data': tasks_by_status})


@main.route('/tasks_status/<int:status_id>/sprints/<int:sprint_id>/tasks')
def get_tasks_by_status_id_and_sprint_id(status_id, sprint_id):
    tasks = Tasks.query.filter(Tasks.status_id == status_id and Tasks.sprint_id == sprint_id).all()
    return jsonify({'success': True, 'data': tasks})


@main.route('/tasks_status', methods=['POST'])
@jwt_required(fresh=True)
def post_status():
    data = request.json
    status_id = data.get('status_id', None)
    if status_id:
        return {'success': False,
                'error': 'Should not have status id',
                'code': 409}, 409
    status_name = data.get('status_name', None)
    if not status_name:
        return {'success': False,
                'error': 'Missing status name',
                'code': 409}, 409
    status = Task_Status(status_id=status_id, status_name=status_name)
    db.session.add(status)
    db.session.commit()
    return jsonify({'success': True, 'data': status}, 200)


@main.route('/tasks_status/<int:status_id>', methods=['PUT'])
@jwt_required(fresh=True)
def put_status(status_id):
    status = Task_Status.query.get_or_404(status_id)
    data = request.json
    status_id = data.get('status_id', None)
    if status_id:
        return {'success': False,
                'error': 'Should not have status id to payload',
                'code': 408}, 408
    status.status_name = data.get('status_name', status.status_name)
    db.session.add(status)
    db.session.commit()
    return jsonify({'success': True, 'data': status}, 200)


@main.route('/tasks_status/<int:status_id>', methods=['DELETE'])
@jwt_required(fresh=True)
def delete_status(status_id):
    result = db.session.execute(db.delete(Task_Status).where(Task_Status.status_id == status_id))
    db.session.commit()
    if result.rowcount == 1:
        return jsonify({'success': True, 'data': f'Status {status_id} deleted'})
    else:
        abort(404)
