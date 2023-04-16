from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required

from . import main
from .. import db
from ..models import Tasks


@main.route('/tasks')
def get_tasks():
    tasks = Tasks.query.all()
    return jsonify({'success': True, 'data': tasks})


@main.route('/tasks/<int:task_id>')
def get_task_by_id(task_id):
    task = Tasks.query.get_or_404(task_id)
    return jsonify({'success': True, 'data': task})


@main.route('/tasks', methods=['POST'])
def post_task():
    data = request.json
    task_id = data.get('task_id', None)
    if task_id:
        return {'success': False,
                'error': 'Should not have task id',
                'code': 409}, 409
    description = data.get('description', None)
    if not description:
        return {'success': False,
                'error': 'Missing description',
                'code': 409}, 409
    user_id = data.get('user_id', None)
    if not user_id:
        return {'success': False,
                'error': 'Missing user id',
                'code': 409}, 409
    sprint_id = data.get('sprint_id', None)
    if not sprint_id:
        return {'success': False,
                'error': 'Missing sprint id',
                'code': 409}, 409
    p_id = data.get('p_id', None)
    if not p_id:
        return {'success': False,
                'error': 'Missing priority id',
                'code': 409}, 409
    status_id = data.get('status_id', None)
    if not status_id:
        return {'success': False,
                'error': 'Missing status id',
                'code': 409}, 409
    tasks = Tasks(task_id=task_id, description=description, user_id=user_id, sprint_id=sprint_id, p_id=p_id,
                  status_id=status_id)
    db.session.add(tasks)
    db.session.commit()
    return jsonify({'success': True, 'data': tasks}, 200)


@main.route('/tasks/<int:task_id>', methods=['PUT'])
def put_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    data = request.json
    task_id = data.get('task_id', None)
    if task_id:
        return {'success': False,
                'error': 'Should not have task id to payload',
                'code': 408}, 408
    task.description = data.get('description', task.description)
    task.user_id = data.get('user_id', task.user_id)
    task.sprint_id = data.get('sprint_id', task.sprint_id)
    task.p_id = data.get('p_id', task.p_id)
    task.status_id = data.get('status_id', task.status_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({'success': True, 'data': task}, 200)


@main.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = db.session.execute(db.delete(Tasks).where(Tasks.task_id == task_id))
    db.session.commit()
    if result.rowcount == 1:
        return jsonify({'success': True, 'data': f'Task {task_id} deleted'})
    else:
        abort(404)
