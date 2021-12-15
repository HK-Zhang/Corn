from flask import Flask, url_for, jsonify, abort, request,send_from_directory,send_file
from flasgger import swag_from
from app.models import Todo, db
from app.common import InvalidUsage
from config import get_sas
from . import api
from ai import *
import logging
import uuid
import io
import os
import json
# logger = logging.getLogger("globallogger")

def replace_id_to_uri(task):
    return dict(uri=url_for('api.get_task', task_id=task.id, _external=True),
                title=task.title,
                description=task.description,
                done=task.done)


@api.route('/todo/api/todo/', methods=['GET'])
@swag_from('get_todo.yaml')
def get_todos():
    try:
      t = hel("Henry")
      b = get_sas()
      a = 1/0
      return jsonify({'todo': t})
    except Exception:
      error_code = str(uuid.uuid1())
      properties = {'custom_dimensions': {'error_code': error_code}}
      logging.exception('Captured an exception.', extra=properties)
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
    raise InvalidUsage('This view is gone', status_code=500)
    return jsonify({'tasks': list(map(replace_id_to_uri, tasks))})

@api.route('/todo/api/upload/', methods=['POST'])
@swag_from('upload.yaml')
def upload_files():
  imageInCloud = False
  if not request.json:
      requestjson = json.loads(request.form["body"])
  else:
    requestjson=request.json
    imageInCloud = True

  dirPath = requestjson['path']
  filename = requestjson['fileName']
  # thickness = requestjson['thickness']
  # rule = requestjson['rule']
  # accLevel = requestjson['accLevel']


  # thickness = json.loads(request.form["body"])
  # t =  thickness["t"] if 't' in thickness else None
  films = requestjson['films']

  for filmName in films:
    f = request.files[filmName]
    current_dir = os.path.dirname(os.path.realpath(__file__))
    f.save(os.path.join(current_dir, filmName))


  # f = request.files['image']
  # current_dir = os.path.dirname(os.path.realpath(__file__))
  # f.save(os.path.join(current_dir, "demo.jpg"))

  with open(os.path.join(current_dir, "result.zip"),'rb') as f:
    g=io.BytesIO(f.read())

  os.remove(os.path.join(current_dir, "result.zip"))
  return send_file(g, as_attachment=True,
                     attachment_filename="result.zip",
                     mimetype="application/zip")

  # return send_from_directory(current_dir, "result.zip", as_attachment=True)
  # return jsonify({'fileName': f.filename})

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
    return '';
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