from flask import Flask, url_for, jsonify, abort, request
from app.models import Todo, db
from . import api
from ai import *
import logging
import uuid

logger = logging.getLogger("globallogger")

def replace_id_to_uri(task):
    return dict(uri=url_for('api.get_task', task_id=task.id, _external=True),
                title=task.title,
                description=task.description,
                done=task.done)


@api.route('/todo/api/todo/', methods=['GET'])
def get_todos():
    """
    This is the todo API
    Call this api passing nothing and get back its result
    ---
    tags:
      - get todos
    responses:
      500:
        description: Error!
      200:
        description: todo Result
        schema:
          id: todo result
          properties:
            todo:
              type: string
              description: task name
              default: null
    """
    try:
      t = hel("Henry")
      a = 1/0
      return jsonify({'todo': t})
    except Exception:
      error_code = uuid.uuid1()
      properties = {'custom_dimensions': {'error_code': error_code}}
      logger.exception('Captured an exception.', extra=properties)
      return f'error_code:{error_code}',500,{"error_code": "abcs"}

@api.route('/todo/api/tasks/', methods=['GET'])
def get_tasks():
    """
    This is the todo API
    Call this api passing nothing and get back its result
    ---
    tags:
      - get todos
    responses:
      500:
        description: Error!
      200:
        description: task list Result
        schema:
          id: task list
          properties:
            tasks:
              type: object
              description: task list
              default: null
    """
    tasks = Todo.query.all()
    return jsonify({'tasks': list(map(replace_id_to_uri, tasks))})


@api.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    This is the todo API
    Call this api passing nothing and get back its result
    ---
    tags:
      - get todos
    parameters:
      - name: task_id
        in: query
        type: integer
        description: task id
    responses:
      500:
        description: Error!
      200:
        description: task Result
        schema:
          id: task
          properties:
            task:
              type: string
              description: task name
              default: null
    """
    task = Todo.query.filter_by(id=task_id).first()
    if task is None:
        abort(404)

    return jsonify({'task': replace_id_to_uri(task)})


@api.route('/todo/api/tasks/', methods=['POST'])
def create_task():
    """
    This is the todo API
    Call this api passing nothing and get back its result
    ---
    tags:
      - create task
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: task
          required:
            -path
          properties:
            title:
              type: string
              description: title
            description:
              type: string
              description: description
    responses:
      500:
        description: Error!
      200:
        description: task Result
        schema:
          id: task
          properties:
            task:
              type: object
              description: task object
              default: null
    """
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