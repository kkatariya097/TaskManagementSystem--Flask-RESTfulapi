CREATE TABLE task(
    task_id integer primary key autoincrement,
    description text not null,
    user_id integer not null,
    sprint_id integer not null,
    p_id integer not null,
    status_id integer not null,
    foreign key (user_id) references users(user_id),
    foreign key (sprint_id) references sprints(sprint_id),
    foreign key (p_id) references priorities(p_id),
    foreign key (status_id) references task_status(status_id)
);

drop table task;

CREATE TABLE priorities(
    p_id integer primary key autoincrement,
    priority text not null
);

CREATE TABLE project(
    project_id integer primary key autoincrement,
    project_name text not null,
    sub_dates date not null,
    total_sprints int not null
);

ALTER TABLE project DROP COLUMN sub_dates;

drop table project;

CREATE TABLE users(
    user_id integer primary key autoincrement,
    first_name text not null,
    last_name text not null,
    email text not null
);
drop table users;

CREATE TABLE sprints(
    sprint_id integer primary key autoincrement,
    project_id int not null,
    foreign key (project_id) references project(project_id)
);

drop table sprints;

CREATE TABLE task_status(
    status_id integer primary key autoincrement,
    status_name text not null
);

