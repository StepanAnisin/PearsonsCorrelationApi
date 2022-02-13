from flask import Flask, request
from flask_restful import Api
from flask import jsonify
from celery import Celery
import ast

app = Flask(__name__)
celery_app = Celery('celery_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
api = Api(app)


@app.route('/correlation', methods=['GET'])
def correlation_task():
    user_id = request.args.get('user_id', type=int)
    x_data_type = request.args.get('x_data_type', type=str)
    y_data_type = request.args.get('y_data_type', type=str)
    if user_id is None or x_data_type is None or y_data_type is None:
        return jsonify({'Result': 'Bad request', 'Message': "Not enough data"
                                                               " to complete request"}), 404
    app.logger.info("Invoking Method ")
    r = celery_app.send_task('tasks.correlation', kwargs={'x_data_type': f"{x_data_type}", 'y_data_type': f"{y_data_type}", 'user_id':f"{user_id}"})
    app.logger.info(r.backend)
    return jsonify({'Result': 'Task queued', 'Task id': f"{r.id}" }), 200

@app.route('/calculate', methods=['POST'])
def calculate_task():
    # convert bytes to dict
    request_data = request.data
    dict_str = request_data.decode("UTF-8")
    data = ast.literal_eval(dict_str)
    app.logger.info("Invoking Method ")
    r = celery_app.send_task('tasks.calculate', kwargs={'request': data})
    app.logger.info(r.backend)
    return jsonify({'Result': 'Task queued', 'Task id': f"{r.id}" }), 200

@app.route('/task-status/<task_id>')
def get_status(task_id):
    status = celery_app.AsyncResult(task_id, app=celery_app)
    print("Invoking Method ")
    return jsonify({'Status of the Task': f"{str(status.state)}"}), 200

@app.route('/task-result/<task_id>')
def task_result(task_id):
    result = celery_app.AsyncResult(task_id).result
    return jsonify({'Result of the Task': f"{str(result)}"}), 200