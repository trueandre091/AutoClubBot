import os
import sqlite3
from datetime import datetime

DATABASE_DIR = os.path.dirname(__file__)
DATABASE_NAME = "DataBase.db"
DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_NAME)


def create_connection():
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)

    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    table_creation_query = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        name text NOT NULL,
                                        car_brand text NOT NULL,
                                        car_drive text check(car_drive IN ('FWD', 'RWD', 'AWD')),
                                        car_power integer NOT NULL,
                                        car_number text NOT NULL,
                                        entry_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        last_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); """
    try:
        cursor.execute(table_creation_query)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_logs_table():
    conn = create_connection()
    cursor = conn.cursor()
    table_creation_query = """ CREATE TABLE IF NOT EXISTS logs (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        user_id integer NOT NULL,
                                        event text NOT NULL,
                                        info text NOT NULL,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); """
    try:
        cursor.execute(table_creation_query)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_events_table():
    conn = create_connection()
    cursor = conn.cursor()
    table_creation_query = """ CREATE TABLE IF NOT EXISTS events (
                                        event_id integer PRIMARY KEY AUTOINCREMENT,
                                        admin_id integer NOT NULL,
                                        name text NOT NULL,
                                        date DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        place text NOT NULL,
                                        info text NOT NULL,
                                        members text NOT NULL,
                                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); """
    try:
        cursor.execute(table_creation_query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создани таблички мероприятий: {e}")
    finally:
        if conn:
            conn.close()


def add_event(admin_id, name="", date="", place="", info="", members=""):
    conn = create_connection()
    sql = ''' INSERT INTO events(name, date, place, info, admin_id, members)
                  VALUES(?,?,?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, date, place, info, admin_id, members))
        conn.commit()
        event_id = cursor.lastrowid
        return event_id
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении мероприятия: {e}")
    finally:
        if conn:
            conn.close()


def get_event_by_id(event_id):
    conn = create_connection()
    sql = 'SELECT * FROM events WHERE event_id=?'
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (event_id,))
        event = cursor.fetchone()
        return event
    except sqlite3.Error as e:
        print(f"Ошибка при получении мероприятия: {e}")
    finally:
        if conn:
            conn.close()


def update_event(event_id, name=None, date=None, place=None, info=None, admin_id=None, members=None):
    conn = create_connection()
    sql = ''' UPDATE events
                  SET admin_id = ?,
                      name = ?,
                      date = ?,
                      place = ?,
                      info = ?,
                      members = ?
                  WHERE event_id = ?'''
    try:
        cursor = conn.cursor()
        current_event = get_event_by_id(event_id)
        if not current_event:
            print("Event not found.")
            return

        data = (
            admin_id if admin_id is not None else current_event[1],
            name if name is not None else current_event[2],
            datetime.strptime(date, '%d.%m.%Y %H:%M') if date is not None else current_event[3],
            place if place is not None else current_event[4],
            info if info is not None else current_event[5],
            members if members is not None else current_event[6],
            event_id,
        )

        cursor.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def delete_event(event_id):
    conn = create_connection()
    cursor = conn.cursor()

    sql_query = '''DELETE FROM events WHERE event_id = ?'''

    try:
        cursor.execute(sql_query, (event_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при удалении мероприятия: {e}")
    finally:
        if conn:
            conn.close()


def add_user(user_id, username, name="", car_brand="", car_drive="FWD", car_power=0, car_number=""):
    conn = create_connection()
    sql = ''' INSERT INTO users(id, username, name, car_brand, car_drive, car_power, car_number)
              VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, username, name, car_brand, car_drive, car_power, car_number))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя в базу данных: {e}")
    finally:
        if conn:
            conn.close()


def add_log(user_id, event, info=""):
    conn = create_connection()
    sql = ''' INSERT INTO logs(user_id, event, info)
              VALUES(?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, event, info))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении лога: {e}")
    finally:
        if conn:
            conn.close()


def get_all_users():
    """Retrieve all users and their data from the database."""
    conn = create_connection()
    sql = 'SELECT * FROM users'
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        all_users = cursor.fetchall()
        return all_users
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def update_user(user_id, username=None, name=None, car_brand=None, car_drive=None, car_power=None, car_number=None,
                last_timestamp=datetime.now()):
    conn = create_connection()
    sql = ''' UPDATE users
              SET username = ?,
                  name = ?,
                  car_brand = ?,
                  car_drive = ?,
                  car_power = ?,
                  car_number = ?,
                  last_timestamp = ?
              WHERE id = ?'''
    try:
        cursor = conn.cursor()
        current_user = get_user_by_id(user_id)
        if not current_user:
            print("User not found.")
            return

        data = (
            username if username is not None else current_user[1],
            name if name is not None else current_user[2],
            car_brand if car_brand is not None else current_user[3],
            car_drive if car_drive is not None else current_user[4],
            car_power if car_power is not None else current_user[5],
            car_number if car_number is not None else current_user[6],
            last_timestamp,
            user_id,
        )

        cursor.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def get_user_by_id(user_id):
    conn = create_connection()
    sql = 'SELECT * FROM users WHERE id=?'
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_table()
    create_logs_table()
    create_events_table()
