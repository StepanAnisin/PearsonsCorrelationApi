from flask import Flask, request, jsonify
from flask_restful import Api
from business_logic import *
from data_storage_logic import *

app = Flask(__name__)
api = Api(app)

#TODO обернуть всё в try catch и покрыть тестами
@app.route('/calculate', methods=['POST'])
def calculate():
    json = request.json
    print(json)
    result = parse_and_calculate(json)
    #result["user_id"] - user_id
    #result["value"] - Pearson’s correlation coefficient
    #result["p_value"] - p-value
    #result["x_data_type"] - x_data_type
    #result["y_data_type"] - y_data_type
    create_or_update_stat(result["user_id"], result["value"], result["p_value"], result["x_data_type"], result["y_data_type"])
    return jsonify({'Calculated Data:':
                        {
                         'user_id': result["user_id"],
                         'Pearson’s correlation coefficient': result["value"],
                         'p-value': result["p_value"],
                         'x_data_type': result["x_data_type"],
                         'y_data_type': result["y_data_type"],
                         }
                    }), 200


if __name__ == "__main__":
    app.run(debug=True)