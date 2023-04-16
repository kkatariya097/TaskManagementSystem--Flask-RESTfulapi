import os
from sqlalchemy import text
from app import create_app, db
from app.models import Tasks, Task_Status, Priorities, Sprints, Projects, Users
from flask_jwt_extended import JWTManager

app = create_app()

jwt = JWTManager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Tasks=Tasks, Task_Status=Task_Status, Priorities=Priorities, Sprints=Sprints,
                Projects=Projects, Users=Users)


@app.route('/')
def welcome():
    return 'Welcome to Task management!'
    # try:
    #     db.session.query(text('1')).from_statement(text('SELECT 1')).all()
    #     return '<h1>Welcome to Tasks management.</h1>'
    # except Exception as e:
    #     error_text = "<p>The error:<br>" + str(e) + "</p>"
    #     hed = '<h1>Something is broken.</h1>'
    #     return hed + error_text


if __name__ == '__main__':
    app.run()
