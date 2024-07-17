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


def create_events_table():
    conn = create_connection()
    cursor = conn.cursor()
    table_creation_query = """ CREATE TABLE IF NOT EXISTS events (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        admin_id integer NOT NULL,
                                        name text NOT NULL,
                                        date DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        place text NOT NULL,
                                        info text NOT NULL,
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


def create_user_event_table():
    conn = create_connection()
    cursor = conn.cursor()
    table_creation_query = """ CREATE TABLE IF NOT EXISTS user_event (
                                        user_id INTEGER,
                                        event_id INTEGER,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                                        FOREIGN KEY (event_id) REFERENCES events (event_id),
                                        PRIMARY KEY (user_id, event_id)
                                    ); """
    try:
        cursor.execute(table_creation_query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создани таблички связки: {e}")
    finally:
        if conn:
            conn.close()


def add_event(admin_id, name="", date="", place="", info=""):
    conn = create_connection()
    sql = ''' INSERT INTO events(name, date, place, info, admin_id)
                  VALUES(?,?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, date, place, info, admin_id))
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
    sql = 'SELECT * FROM events WHERE id=?'
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


def update_event(event_id, name=None, date=None, place=None, info=None, admin_id=None):
    conn = create_connection()
    sql = ''' UPDATE events
                  SET admin_id = ?,
                      name = ?,
                      date = ?,
                      place = ?,
                      info = ?
                  WHERE id = ?'''
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

    sql_query = '''DELETE FROM events WHERE id = ?'''

    try:
        cursor.execute(sql_query, (event_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при удалении мероприятия: {e}")
    finally:
        if conn:
            conn.close()


def get_all_events_after(date):
    conn = create_connection()
    sql = ('SELECT * FROM events '
           'WHERE date > ?')
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (date,))
        all_events = cursor.fetchall()
        return all_events
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def add_user(user_id, username, name="", car_brand="", car_drive="FWD", car_power=0, car_number=""):
    conn = create_connection()
    sql = ''' INSERT INTO users(id, username, name, car_brand, car_drive, car_power, car_number)
              VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING'''

    try:
        cursor = conn.cursor()
        cursor.execute(sql, (
        user_id, username if username is not None else " ", name, car_brand, car_drive, car_power, car_number))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя в базу данных: {e}")
    finally:
        if conn:
            conn.close()


def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    user_id = int(user_id)
    try:
        cursor.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
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


# Функция, возвращающая всех участников одного мероприятия
def get_event_users(event_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, name, car_brand, car_drive, car_power, car_number FROM users
        INNER JOIN user_event ON users.id = user_event.user_id
        WHERE event_id = ?
    ''', (event_id,))

    users = [row for row in cursor.fetchall()]

    conn.close()
    return users


# Функция, возвращающая все мероприятия, в которых участвует один участник
def get_user_events(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, admin_id, name, date, place, info, created_at FROM events
        INNER JOIN user_event ON events.id = user_event.event_id
        WHERE user_id = ?
    ''', (user_id,))

    events = [row for row in cursor.fetchall()]

    conn.close()
    return events


# Функция, добавляющая связь участник - мероприятие
def add_user_to_event(user_id, event_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO user_event (user_id, event_id) VALUES (?, ?)
    ''', (user_id, event_id))

    conn.commit()
    conn.close()


# Функция, удаляющая связь участник - мероприятие
def remove_user_from_event(user_id, event_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM user_event WHERE user_id = ? AND event_id = ?
    ''', (user_id, event_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    create_events_table()
    create_user_event_table()
