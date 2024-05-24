# app.py
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from model.tasks import task
task_api = Blueprint('task_api', __name__,
                   url_prefix='/api/tasks')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        data = request.json
        new_task = Task(content=data['content'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully!'}), 201
    else:
        tasks = Task.query.all()
        result = [{'id': task.id, 'content': task.content, 'completed': task.completed} for task in tasks]
        return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
