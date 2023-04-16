from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required

from . import main
from .. import db
from ..models import Priorities, Tasks, Sprints


@main.route('/priorities')
def get_priorities():
    priorities = Priorities.query.all()
    return jsonify({'success': True, 'data': priorities})


@main.route('/priorities/<int:p_id>')
def get_priority_by_id(p_id):
    priority = Priorities.query.get_or_404(p_id)
    return jsonify({'success': True, 'data': priority})


@main.route('/priorities/<int:p_id>/tasks')
def get_tasks_by_priority_id(p_id):
    tasks_by_priority = Tasks.query.filter(Tasks.p_id == p_id).all()
    return jsonify({'success': True, 'data': tasks_by_priority})


@main.route('/priorities/<int:p_id>/sprints/<int:sprint_id>/tasks')
def get_tasks_by_priority_id_and_sprint_id(p_id, sprint_id):
    tasks = Tasks.query.filter(Tasks.p_id == p_id, Tasks.sprint_id == sprint_id).all()
    return jsonify({'success': True, 'data': tasks})


@main.route('/priorities', methods=['POST'])
def post_priority():
    data = request.json
    p_id = data.get('p_id', None)
    if p_id:
        return {'success': False,
                'error': 'Should not have priority id',
                'code': 409}, 409
    priority = data.get('priority', None)
    if not priority:
        return {'success': False,
                'error': 'Missing priority',
                'code': 409}, 409
    priorities = Priorities(p_id=p_id, priority=priority)
    db.session.add(priorities)
    db.session.commit()
    return jsonify({'success': True, 'data': priorities}, 200)


@main.route('/priorities/<int:p_id>', methods=['PUT'])
def put_priority(p_id):
    priority = Priorities.query.get_or_404(p_id)
    data = request.json
    p_id = data.get('p_id', None)
    if p_id:
        return {'success': False,
                'error': 'Should not have priority id to payload',
                'code': 408}, 408
    priority.priority = data.get('priority', priority.priority)
    db.session.add(priority)
    db.session.commit()
    return jsonify({'success': True, 'data': priority}, 200)


@main.route('/priorities/<int:p_id>', methods=['DELETE'])
def delete_priority(p_id):
    result = db.session.execute(db.delete(Priorities).where(Priorities.p_id == p_id))
    db.session.commit()
    if result.rowcount == 1:
        return jsonify({'success': True, 'data': f'Priority {p_id} deleted'})
    else:
        abort(404)
