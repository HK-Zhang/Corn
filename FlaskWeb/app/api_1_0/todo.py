from flask import Flask, url_for, jsonify, abort, request
from app.models import Todo, db
from . import api
from ai import *

def replace_id_to_uri(task):
    return dict(uri=url_for('api.get_task', task_id=task.id, _external=True),
                title=task.title,
                description=task.description,
                done=task.done)


@api.route('/todo/api/todo/', methods=['GET'])
def get_todos():
    t = hel("Henry")
    return jsonify({'todo': t})

@api.route('/todo/api/tasks/', methods=['GET'])
def get_tasks():
    tasks = Todo.query.all()
    return jsonify({'tasks': list(map(replace_id_to_uri, tasks))})


@api.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    if task is None:
        abort(404)

    return jsonify({'task': replace_id_to_uri(task)})


@api.route('/todo/api/tasks/', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task = Todo(request.json['title'], request.json.get('description', ""),
                False)

    db.session.add(task)
    db.session.commit()
    return jsonify({'task': replace_id_to_uri(task)}), 201


@api.route('/todo/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    if task is None:
        abort(404)

    if not request.json:
        abort(400)
    if 'title' in request.json:
        abort(400)
    if 'description' in request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['done'] = request.json.get('done', task['done'])

    #db.session.update(task)
    db.session.commit()
    return jsonify({'task': replace_id_to_uri(task)})

@api.route('/todo/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    if task is None:
        abort(404)
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})