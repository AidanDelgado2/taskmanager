from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify, current_app, Response, g
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import Post
app = Flask(__name__)
task_api = Blueprint('task_api', __name__,
                   url_prefix='/api/tasks')

api = Api(task_api)

# Configure the SQLite database, relative to the app instance folder
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

class TaskResource(Resource):
    def get(self, task_id):
        task = Post.query.get(task_id)
        if task:
            return jsonify(task.read())
        return {"message": "Task not found"}, 404

    def post(self):
        data = request.get_json()
        new_task = Post(id=data['userID'], task=data['task'], duedate=data['duedate'])
        created_task = new_task.create()
        if created_task:
            return jsonify(created_task.read())
        return {"message": "Task could not be created"}, 500

# Add Resource to API
api.add_resource(TaskResource, '/')

if __name__ == '__main__':
    app.run(debug=True)