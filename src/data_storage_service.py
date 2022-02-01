import psycopg2
import json

with open('config.json', 'r') as config_file:
    data = json.load(config_file)

host = data['host']
database = data['database']
user = data['user']
password = data['password']
port = data['port']
users_stat_table = data['users_stat_table']

def create_or_update_stat(user_id: int, value: float, p_value: float, x_data_type: str, y_data_type: str):
    # try to get statistics by user_id
    rows = execute_command(f"select * from {users_stat_table} "
                                 f"where user_id = {user_id}")
    #if there is no statistics about user with such id
    if len(rows) == 0:
        # insert a new row into table
        execute_command(f"insert into {users_stat_table}(user_id, x_data_type, y_data_type, p_value, value) "
                        f"values ({user_id},'{x_data_type}','{y_data_type}',{p_value},{value}) "
                        f"returning user_id")
    else:
        # if user exists update values
        execute_command(f"update {users_stat_table} "
                              f"set x_data_type = '{x_data_type}', "
                              f"y_data_type = '{y_data_type}', "
                              f"p_value = {p_value}, "
                              f"value = {value} "
                              f"where user_id = {user_id} "
                              f"returning user_id ")

def execute_command(command):
    try:
        # open the connection
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(command)
        rows = cursor.fetchall()
        # close the connection
        connection.close()
        return rows
    except SystemError:
            raise SystemError("Incorrect data format, should be YYYY-MM-DD")