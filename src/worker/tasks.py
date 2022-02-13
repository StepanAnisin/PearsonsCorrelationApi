from business_logic_service import *
from celery import Celery
from celery.utils.log import get_task_logger
from data_storage_service import *
import json

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.task(serializer='pickle')
def calculate(request: dict):
    try:
        result = parse_and_calculate(request)
        create_or_update_stat(result["user_id"], result["value"],
                              result["p_value"], result["x_data_type"], result["y_data_type"])
    except (ValueError, KeyError, TypeError, SystemError) as e:
        return json.dumps({'Result': 'Bad request', 'Message': str(e)}), 500
    else:
        return json.dumps({
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

@app.task(serializer='pickle')
def correlation(x_data_type: str, y_data_type: str, user_id: int):
    rows = get_correlation_by_parameters(x_data_type, y_data_type, user_id)
    if len(rows) == 0:
        return json.dumps({'Result': 'Bad request', 'Message': "No data for given parameters"}), 400
    else:
        return json.dumps({'Result':'Success',
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