import datetime
from scipy import stats

def parse_and_calculate(request_data: dict):
    # parse our data
    user_id, data_x, data_y, x_data_type, y_data_type = parse_data(request_data)
    # dictionary with matched date as a key and values from x and y (less or greater than 2 values per 1 date)
    matched_data = intersect(data_x, data_y)
    # here we split and filter data into two list for further calculations
    first_list, second_list = split_into_two_lists(matched_data)
    # calculate pearsons correlation
    stat = pearsons_correlation(first_list, second_list)
    return {"user_id": user_id, "value": stat[0], "p_value": stat[1], "x_data_type": x_data_type,
            "y_data_type": y_data_type}

def split_into_two_lists(matched_data: dict):
    # skip data with missing or superfluous values
    correct_data = {k: v for k, v in matched_data.items() if len(v) == 2}
    # list with values from x
    first_list = [value[0] for item, value in correct_data.items()]
    # list with values from y
    second_list = [value[1] for item, value in correct_data.items()]
    return first_list, second_list

def is_date_valid(date_text: str):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def parse_data(request_data: dict):
    outer_keys = ["user_id", "data"]
    inner_keys = ["x_data_type", "y_data_type", "x", "y"]
    indicator_keys = ["date", "value"]
    # check if our input dictionary contains all outer keys
    for key in outer_keys:
        if key not in request_data:
            raise KeyError('Data from request has missing keys')
    user_id = request_data["user_id"]
    # get data from our json file
    data = request_data["data"]
    # check if our data dictionary contains all inner keys
    for key in inner_keys:
        if key not in data:
            raise KeyError('Data from request has missing keys')
    # get data from x
    data_x = data["x"]
    # get data from y
    data_y = data["y"]
    # get x data type
    x_data_type = data["x_data_type"]
    # get y data type
    y_data_type = data["y_data_type"]
    # check if types of variables are valid
    if type(user_id) is not int or type(x_data_type) is not str or type(y_data_type) is not str or type(data_x) is not \
            list or type(data_y) is not list:
        raise TypeError('Some of the values in data request has wrong types')
    for item in data_x:
        for key in indicator_keys:
            if key not in item:
                raise KeyError('Data from request has missing keys')
        is_date_valid(item["date"])
        if type(item["value"]) is not float:
            raise ValueError('Some of the values in data request has wrong types')
    return user_id, data_x, data_y, x_data_type, y_data_type


def intersect(a: list, b: list):
    # get all data from first list
    c = {item["date"] : [item["value"]] for item in a}
    for item in b:
        if item["date"] in c:
            # then just append matched data from second list
            c[item["date"]].append(item["value"])
        else:
            c[item["date"]] = [item["value"]]
    return c

def pearsons_correlation(first_array: list, second_array: list):
    if len(first_array) < 2 or len(second_array) < 2:
        raise ValueError('To calculate Pearsons Correlation x and y must have length at least 2.')
    stat = stats.pearsonr(first_array, second_array)
    return stat
