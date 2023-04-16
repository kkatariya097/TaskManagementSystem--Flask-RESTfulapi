from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required

from . import main
from .. import db
from ..models import Sprints, Tasks


@main.route('/sprints')
def get_sprints():
    sprints = Sprints.query.all()
    return jsonify({'success': True, 'data': sprints})


@main.route('/sprints/<int:sprint_id>')
def get_sprint_by_id(sprint_id):
    sprint = Sprints.query.get_or_404(sprint_id)
    return jsonify({'success': True, 'data': sprint})


@main.route('/sprints/<int:sprint_id>/tasks')
def get_tasks_by_sprint_id(sprint_id):
    tasks_by_sprint = Tasks.query.filter(Tasks.sprint_id == sprint_id).all()
    return jsonify({'success': True, 'data': tasks_by_sprint})


@main.route('/sprints', methods=['POST'])
def post_sprints():
    data = request.json
    sprint_id = data.get('sprint_id', None)
    if sprint_id:
        return {'success': False,
                'error': 'Should not have sprint id',
                'code': 409}, 409
    project_id = data.get('project_id', None)
    if not project_id:
        return {'success': False,
                'error': 'Missing project id',
                'code': 409}, 409
    start_date = data.get('start_date', None)
    if not start_date:
        return {'success': False,
                'error': 'Missing start date',
                'code': 409}, 409
    end_date = data.get('end_date', None)
    if not end_date:
        return {'success': False,
                'error': 'Missing end date',
                'code': 409}, 409
    sprints = Sprints(sprint_id=sprint_id, project_id=project_id, start_date=start_date, end_date=end_date)
    db.session.add(sprints)
    db.session.commit()
    return jsonify({'success': True, 'data': sprints}, 200)


@main.route('/sprints/<int:sprint_id>', methods=['PUT'])
def put_sprint(sprint_id):
    sprint = Sprints.query.get_or_404(sprint_id)
    data = request.json
    sprint_id = data.get('project_id', None)
    if sprint_id:
        return {'success': False,
                'error': 'Should not have sprint id to payload',
                'code': 408}, 408
    sprint.project_id = data.get('project_id', sprint.project_id)
    sprint.start_date = data.get('start_date', sprint.start_date)
    sprint.end_date = data.get('end_date', sprint.end_date)
    db.session.add(sprint)
    db.session.commit()
    return jsonify({'success': True, 'data': sprint}, 200)


@main.route('/sprints/<int:sprint_id>', methods=['DELETE'])
def delete_sprints(sprint_id):
    result = db.session.execute(db.delete(Sprints).where(Sprints.sprint_id == sprint_id))
    db.session.commit()
    if result.rowcount == 1:
        return jsonify({'success': True, 'data': f'Sprint {sprint_id} deleted'})
    else:
        abort(404)
