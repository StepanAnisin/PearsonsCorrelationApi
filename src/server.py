from flask import Flask, request, jsonify
from flask_restful import Api
from business_logic_service import *
from data_storage_service import *

app = Flask(__name__)
api = Api(app)

# TODO обернуть всё в try catch и покрыть тестами


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        json = request.json
        result = parse_and_calculate(json)
    except (ValueError, KeyError, TypeError) as e:
        return jsonify({'Result': 'Bad request', 'Message': str(e)}), 400
    else:
        # result["user_id"] - user_id
        # result["value"] - Pearson’s correlation coefficient
        # result["p_value"] - p-value
        # result["x_data_type"] - x_data_type
        # result["y_data_type"] - y_data_type
        try:
            create_or_update_stat(result["user_id"], result["value"],
                                  result["p_value"], result["x_data_type"], result["y_data_type"])
        except Exception:
            return jsonify({'Result': 'Bad request', 'Message': 'Error while saving data in database'}), 500
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