import psycopg2
from db_config import DB_DATABASE, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER


def link_to_bdd():
    try:
        connection = psycopg2.connect(database = DB_DATABASE,
                                      host = DB_HOST,
                                      password = DB_PASSWORD,
                                      port = DB_PORT,
                                      user = DB_USER
        )
        connection.autocommit = True
        cursor = connection.cursor()
        print('Connection to the BBD successful')
        return connection, cursor
    except psycopg2.Error as e:
        print(f'Error: Enable to connect to Database! {e}')
        return None, None
    

def create_tables():
    connection, cursor = link_to_bdd()
    if connection is None or cursor is None:
        print('Unable to create the tables!')
        return
    try:
        cursor.execute('DROP TABLE IF EXISTS meals')
        meals_query = '''create table meals(
                        id serial primary key,
                        meal_name text not NULL,
                        calories INT,
                        date DATE default current_date
                        )'''
        cursor.execute(meals_query)
        cursor.execute('DROP TABLE IF EXISTS workout')
        workout_query = '''create table workout(
                            id serial primary key,
                            workout_name text not NULL,
                            calories int,
                            date DATE Default current_date
                        )'''
        cursor.execute(workout_query)
    except Exception as e:
        print(f'Error during the creation of the table {e}')
    finally:
        cursor.close()
        connection.close()
        print('The Tables have been created')


