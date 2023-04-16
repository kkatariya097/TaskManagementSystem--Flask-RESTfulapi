from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required
import datetime

from . import main
from .. import db
from ..models import Projects, Sprints


@main.route('/projects')
def get_projects():
    projects = Projects.query.all()
    return jsonify({'success': True, 'data': projects})


@main.route('/projects/<int:project_id>')
def get_project_by_id(project_id):
    project = Projects.query.get_or_404(project_id)
    return jsonify({'success': True, 'data': project})


@main.route('/projects/<int:project_id>/sprints')
def get_sprints_by_project_id(project_id):
    sprints_by_project = Sprints.query.filter(Sprints.project_id == project_id).all()
    return jsonify({'success': True, 'data': sprints_by_project})


@main.route('/projects', methods=['POST'])
def post_poject():
    data = request.json
    project_id = data.get('project_id', None)
    if project_id:
        return {'success': False,
                'error': 'Should not have project id',
                'code': 409}, 409
    project_name = data.get('project_name', None)
    if not project_name:
        return {'success': False,
                'error': 'Missing project name',
                'code': 409}, 409
    sub_dates = data.get('sub_dates', None)
    if not sub_dates:
        return {'success': False,
                'error': 'Missing submission dates',
                'code': 409}, 409
    total_sprints = data.get('total_sprints', None)
    if not total_sprints:
        return {'success': False,
                'error': 'Missing total sprints',
                'code': 409}, 409
    projects = Projects(project_id=project_id, project_name=project_name, sub_dates=sub_dates,
                        total_sprints=total_sprints)
    db.session.add(projects)
    db.session.commit()
    return jsonify({'success': True, 'data': projects}, 200)


@main.route('/projects/<int:project_id>', methods=['PUT'])
def put_project(project_id):
    project = Projects.query.get_or_404(project_id)
    data = request.json
    project_id = data.get('project_id', None)
    if project_id:
        return {'success': False,
                'error': 'Should not have project id to payload',
                'code': 408}, 408
    project.project_name = data.get('project_name', project.project_name)
    project.sub_dates = data.get('sub_dates', project.sub_dates)
    project.total_sprints = data.get('total_sprints', project.total_sprints)
    db.session.add(project)
    db.session.commit()
    return jsonify({'success': True, 'data': project}, 200)


@main.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    result = db.session.execute(db.delete(Projects).where(Projects.project_id == project_id))
    db.session.commit()
    if result.rowcount == 1:
        return jsonify({'success': True, 'data': f'Project {project_id} deleted'})
    else:
        abort(404)
