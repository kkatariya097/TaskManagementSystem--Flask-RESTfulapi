from flask import render_template, request, jsonify
from . import main
from ..models import Tasks, Priorities, Projects, Users, Sprints, Task_Status
from . import views_task, views_priorities, views_project, views_users, views_sprints, views_task_status


@main.errorhandler(404)
def errorHandler(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'msg': error.name})
        response.status_code = error.code
        return response
    return render_template('error.html', error=error), error.code
