import json
from app import db


class TaskEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Tasks):
            return {'task_id': o.task_id,
                    'description': o.description,
                    'user_id': o.user_id,
                    'sprint_id': o.sprint_id,
                    'p_id': o.p_id,
                    'status_id': o.status_id
                    }
        elif isinstance(o, Priorities):
            return {'p_id': o.p_id,
                    'priority': o.priority
                    }
        elif isinstance(o, Projects):
            return {'project_id': o.project_id,
                    'project_name': o.project_name,
                    'sub_dates': o.sub_dates,
                    'total_sprints': o.total_sprints
                    }
        elif isinstance(o, Users):
            return {'user_id': o.user_id,
                    'first_name': o.first_name,
                    'last_name': o.last_name,
                    'email': o.email
                    }
        elif isinstance(o, Sprints):
            return {'sprint_id': o.sprint_id,
                    'project_id': o.project_id
                    }
        elif isinstance(o, Task_Status):
            return {'status_id': o.status_id,
                    'status_name': o.status_name
                    }

        else:
            return super().default(o)


class Tasks(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    description = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'), nullable=False)
    sprint_id = db.Column(db.Integer(), db.ForeignKey('sprints.sprint_id'), nullable=False)
    p_id = db.Column(db.Integer(), db.ForeignKey('priorities.p_id'), nullable=False)
    status_id = db.Column(db.Integer(), db.ForeignKey('task_status.status_id'), nullable=False)

    def __repr__(self):  # __functions are known as private
        return f"<task {self.task_id}: {self.description}: {self.user_id}: {self.sprint_id}: {self.p_id}: {self.status_id}>"


class Priorities(db.Model):
    __tablename__ = 'priorities'
    p_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    priority = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<priorities {self.p_id}: {self.priority}>"


class Projects(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_name = db.Column(db.Text(), nullable=False)
    sub_dates = db.Column(db.Text(), nullable=False)
    total_sprints = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"<project {self.project_id}: {self.project_name}: {self.sub_dates}: {self.total_sprints}>"


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text(), nullable=False)
    last_name = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<users {self.user_id}: {self.first_name}: {self.last_name}: {self.email}>"


class Sprints(db.Model):
    __tablename__ = 'sprints'
    sprint_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_id = db.Column(db.Text(), db.ForeignKey('project.project_id'), nullable=False)
    start_date = db.Column(db.Text(), nullable=False)
    end_date = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<sprints {self.sprint_id}: {self.project_id}>"


class Task_Status(db.Model):
    __tablename__ = 'task_status'
    status_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    status_name = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<task_status {self.status_id}: {self.status_name}>"
