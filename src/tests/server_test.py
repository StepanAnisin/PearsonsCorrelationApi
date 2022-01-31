import requests

BASE ="http://127.0.0.1:5000/"

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

test_data6 = {
  "user_id": 42,
  "data": {
    "x_data_type": "sleep_hours",
    "y_data_type": "morning_pulse",
    "x": "test",
    "y": "test"
  }
}
response = requests.post(BASE + "calculate", json=test_data6)
print(response.json())