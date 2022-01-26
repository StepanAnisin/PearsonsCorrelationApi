from scipy import stats

def parse_and_calculate(json):
    #parse our data
    user_id, data, data_x, data_y, x_data_type, y_data_type = parse_data(json)
    #dictionary with matched date as a key and values from x and y (less or greater than 2 values per 1 date)
    matched_data = intersect(data_x, data_y)
    #skip data with missing or superfluous values
    correct_data = {k: v for k, v in matched_data.items() if len(v) == 2}
    #list with values from x
    first_list = [value[0] for item, value in correct_data.items()]
    #list with values from y
    second_list = [value[1] for item, value in correct_data.items()]
    #calculate pearsons correlation
    stat = pearsons_correlation(first_list, second_list)
    return {"user_id": user_id, "value": stat[0], "p_value": stat[1], "x_data_type": x_data_type,
            "y_data_type": y_data_type}

def parse_data(json):
    user_id = json["user_id"]
    # get data from our json file
    data = json["data"]
    # get data from x
    data_x = data["x"]
    # get data from y
    data_y = data["y"]
    # get x data type
    x_data_type = data["x_data_type"]
    # get y data type
    y_data_type = data["y_data_type"]
    return user_id, data, data_x, data_y, x_data_type, y_data_type


def intersect(a: list, b: list):
    #get all data from first list
    c = {item["date"] : [item["value"]] for item in a}
    for item in b:
        if item["date"] in c:
            # then just append matched data from second list
            c[item["date"]].append(item["value"])
        else:
            c[item["date"]] = [item["value"]]
    return c

def pearsons_correlation(first_array, second_array):
    stat = stats.pearsonr(first_array, second_array)
    return stat