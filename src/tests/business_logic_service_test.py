import pytest
from business_logic_service import *


#Case 1:
# 2 values in each list
test_data1 = {
  "user_id": 42,
  "data": {
    "x_data_type": "sleep_hours",
    "y_data_type": "morning_pulse",
    "x": [
      {
        "date": "2022-01-14",
        "value": 9.7
      },
      {
        "date": "2022-01-08",
        "value": 9.0
      }
    ],
    "y": [
      {
        "date": "2022-01-14",
        "value": 45
      },
      {
        "date": "2022-01-08",
        "value": 96
      }
    ]
  }
}

#Case 2:
#Multiple values in each list
test_data2 = {
  "user_id": 43,
  "data": {
    "x_data_type": "temperature",
    "y_data_type": "height",
    "x": [
      {
        "date": "2022-01-05",
        "value": 6.5
      },
      {
        "date": "2022-01-08",
        "value": 8.6
      },
      {
        "date": "2022-02-01",
        "value": 6.0
      },
      {
        "date": "2022-01-26",
        "value": 9.9
      },
      {
        "date": "2022-01-23",
        "value": 5.2
      },
      {
        "date": "2022-01-13",
        "value": 5.3
      }
    ],
    "y": [
      {
        "date": "2022-01-05",
        "value": 60
      },
      {
        "date": "2022-01-08",
        "value": 47
      },
      {
        "date": "2022-02-01",
        "value": 97
      },
      {
        "date": "2022-01-26",
        "value": 93
      },
      {
        "date": "2022-01-23",
        "value": 68
      },
      {
        "date": "2022-01-13",
        "value": 49
      }
    ]
  }
}

#Case 3:
#No values in each lists
test_data3 = {
  "user_id": 44,
  "data": {
    "x_data_type": "pressure",
    "y_data_type": "pulse",
    "x": [],
    "y": []
  }
}

#Case 4:
#X contains less values than Y
test_data4 = {
  "user_id": 44,
  "data": {
    "x_data_type": "pressure",
    "y_data_type": "pulse",
    "x": [
      {
        "date": "2022-02-01",
        "value": 6.5
      },
      {
        "date": "2022-01-11",
        "value": 8.6
      }
    ],
    "y": [
      {
        "date": "2022-02-01",
        "value": 60
      },
      {
        "date": "2022-01-08",
        "value": 47
      },
      {
        "date": "2022-02-01",
        "value": 97
      },
      {
        "date": "2022-01-26",
        "value": 93
      },
      {
        "date": "2022-01-23",
        "value": 68
      },
      {
        "date": "2022-01-13",
        "value": 49
      }
    ]
  }
}

#Case 5:
#Corrupted data
test_data5 = {
  "test": ""
  }

def test_business_logic_service():
    ###
    #Case 1:
    ###
    user_id, data_x, data_y, x_data_type, y_data_type = parse_data(test_data1)
    assert user_id == 42
    assert data_x == [{'date': '2022-01-14', 'value': 9.7}, {'date': '2022-01-08', 'value': 9.0}]
    assert data_y == [{'date': '2022-01-14', 'value': 45}, {'date': '2022-01-08', 'value': 96}]
    assert x_data_type == "sleep_hours"
    assert y_data_type == "morning_pulse"

    matched_data = intersect(data_x, data_y)
    assert matched_data == {'2022-01-14': [9.7, 45], '2022-01-08': [9.0, 96]}
    first_list, second_list = split_into_two_lists(matched_data)
    assert first_list == [9.7, 9.0]
    assert second_list == [45, 96]
    result = pearsons_correlation(first_list, second_list)
    assert result == (-1.0, 1.0)

    ###
    #Case 2:
    ###
    user_id, data_x, data_y, x_data_type, y_data_type = parse_data(test_data2)
    assert user_id == 43
    assert data_x == [{'date': '2022-01-05', 'value': 6.5}, {'date': '2022-01-08', 'value': 8.6},
                      {'date': '2022-02-01', 'value': 6.0}, {'date': '2022-01-26', 'value': 9.9},
                      {'date': '2022-01-23', 'value': 5.2}, {'date': '2022-01-13', 'value': 5.3}]
    assert data_y == [{'date': '2022-01-05', 'value': 60}, {'date': '2022-01-08', 'value': 47},
                      {'date': '2022-02-01', 'value': 97}, {'date': '2022-01-26', 'value': 93},
                      {'date': '2022-01-23', 'value': 68}, {'date': '2022-01-13', 'value': 49}]
    assert x_data_type == "temperature"
    assert y_data_type == "height"
    matched_data = intersect(data_x, data_y)

    assert matched_data == {'2022-01-05': [6.5, 60], '2022-01-08': [8.6, 47],
                            '2022-02-01': [6.0, 97], '2022-01-26': [9.9, 93],
                            '2022-01-23': [5.2, 68], '2022-01-13': [5.3, 49]}
    first_list, second_list = split_into_two_lists(matched_data)
    assert first_list == [6.5, 8.6, 6.0, 9.9, 5.2, 5.3]
    assert second_list == [60, 47, 97, 93, 68, 49]
    assert pearsons_correlation(first_list, second_list) == (0.22630159761052424, 0.6663423290330824)

    ###
    # Case 3:
    ###
    user_id, data_x, data_y, x_data_type, y_data_type = parse_data(test_data3)
    assert user_id == 44
    assert data_x == []
    assert data_y == []
    assert x_data_type == "pressure"
    assert y_data_type == "pulse"
    matched_data = intersect(data_x, data_y)
    assert matched_data == {}
    first_list, second_list = split_into_two_lists(matched_data)
    assert first_list == []
    assert second_list == []
    with pytest.raises(ValueError):
        pearsons_correlation(first_list, second_list)

    ###
    # Case 4:
    ###
    user_id, data_x, data_y, x_data_type, y_data_type = parse_data(test_data4)
    assert user_id == 44
    assert data_x == [{'date': '2022-02-01', 'value': 6.5}, {'date': '2022-01-11', 'value': 8.6}]
    assert data_y == [{'date': '2022-02-01', 'value': 60}, {'date': '2022-01-08', 'value': 47},
                      {'date': '2022-02-01', 'value': 97}, {'date': '2022-01-26', 'value': 93},
                      {'date': '2022-01-23', 'value': 68}, {'date': '2022-01-13', 'value': 49}]
    assert x_data_type == "pressure"
    assert y_data_type == "pulse"

    matched_data = intersect(data_x, data_y)
    assert matched_data == {'2022-02-01': [6.5, 60, 97], '2022-01-11': [8.6],
                            '2022-01-08': [47], '2022-01-26': [93],
                            '2022-01-23': [68], '2022-01-13': [49]}
    first_list, second_list = split_into_two_lists(matched_data)
    assert first_list == []
    assert second_list == []
    with pytest.raises(ValueError):
        pearsons_correlation(first_list, second_list)

    ###
    # Case 5:
    ###
    with pytest.raises(KeyError):
        parse_data(test_data5)


test_business_logic_service()
