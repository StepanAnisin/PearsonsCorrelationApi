from flask import Flask, request, jsonify
from flask_restful import Api
from business_logic_service import *
from data_storage_service import *
from redis_worker import redis_queue

app = Flask(__name__)
api = Api(app)


@app.route('/correlation', methods=['GET'])
def correlation():
    user_id = request.args.get('user_id', type = int)
    x_data_type = request.args.get('x_data_type', type = str)
    y_data_type = request.args.get('y_data_type', type = str)
    if user_id is None or x_data_type is None or y_data_type is None:
        return jsonify({'Result': 'Bad request', 'Message': "Not enough data"
                                                            " to complete request"}), 404
    else:
        rows = get_correlation_by_parameters(x_data_type, y_data_type, user_id)
        if len(rows) == 0:
            return jsonify({'Result': 'Bad request', 'Message': "No data for given parameters"}), 404
        else:
            return jsonify({'Result':'Success',
                            'Data': {
                            'user_id': rows[0][0],
                            'x_data_type': rows[0][1],
                            'y_data_type': rows[0][2],
                            'correlation': {
                                'value': rows[0][3],
                                'p-value': rows[0][4]
                            }
                         }
                        }), 200

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        json = request.json
        result = parse_and_calculate(json)
        # result["user_id"] - user_id
        # result["value"] - Pearson’s correlation coefficient
        # result["p_value"] - p-value
        # result["x_data_type"] - x_data_type
        # result["y_data_type"] - y_data_type
        create_or_update_stat(result["user_id"], result["value"],
                              result["p_value"], result["x_data_type"], result["y_data_type"])
    except (ValueError, KeyError, TypeError, SystemError) as e:
        return jsonify({'Result': 'Bad request', 'Message': str(e)}), 500
    else:
        return jsonify({
            'Result': 'Success',
            'Calculated Data:':
                {
                'user_id': result["user_id"],
                'Pearson’s correlation coefficient': result["value"],
                'p-value': result["p_value"],
                'x_data_type': result["x_data_type"],
                'y_data_type': result["y_data_type"],
            }
        }), 200

def some_function(a: int):
    return jsonify({"HelloWorld"})


@app.route('/test', methods=['GET'])
def test():
    job = redis_queue.enqueue(some_function, 1)
    return jsonify({"Result": "Success", "job_id": job.id}), 200