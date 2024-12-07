import pandas as pd
import mysql.connector
from faker import Faker
import random
from config import DATABASE

import mysql.connector
from config import DATABASE

def create_tables():
    """Создает таблицы с предварительным сбросом."""
    try:
        print("Попытка подключиться к базе данных...")
        conn = mysql.connector.connect(**DATABASE)
        cur = conn.cursor()
        
        
        print("Удаление таблиц, если они существуют...")
        cur.execute("DROP TABLE IF EXISTS Workouts")
        cur.execute("DROP TABLE IF EXISTS Gym_Clients")
        
        
        print("Создание таблиц...")
        cur.execute('''
            CREATE TABLE Gym_Clients (
                client_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                gender ENUM('Male', 'Female', 'Other'),
                membership_type ENUM('Basic', 'Premium', 'VIP')
            )
        ''')
        cur.execute('''
            CREATE TABLE Workouts (
                workout_id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT,
                type ENUM('Cardio', 'Strength', 'Flexibility', 'Balance'),
                duration INT,
                calories_burned FLOAT,
                session_date DATE,
                FOREIGN KEY (client_id) REFERENCES Gym_Clients(client_id)
            )
        ''')
        
        conn.commit()
        print("Таблицы созданы успешно.")
    
    except mysql.connector.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
    
    except Exception as ex:
        print(f"Произошла непредвиденная ошибка: {ex}")
    
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()
            print("Соединение с базой данных закрыто.")



def generate_data(num_clients=10000, num_workouts=5000):
    """Генерирует данные клиентов и тренировок."""
    fake = Faker()
    membership_types = ['Basic', 'Premium', 'VIP']
    genders = ['Male', 'Female', 'Other']

    try:
        conn = mysql.connector.connect(**DATABASE)
        cur = conn.cursor()
        
        
        clients_data = [
            (fake.name(), random.randint(18, 60), random.choice(genders), random.choice(membership_types))
            for _ in range(num_clients)
        ]
        cur.executemany(
            "INSERT INTO Gym_Clients (name, age, gender, membership_type) VALUES (%s, %s, %s, %s)", 
            clients_data
        )
        
        
        cur.execute("SELECT client_id FROM Gym_Clients")
        client_ids = [row[0] for row in cur.fetchall()]
        
        
        workouts_data = [
            (
                random.choice(client_ids),
                random.choice(['Cardio', 'Strength', 'Flexibility', 'Balance']),
                random.randint(20, 120),
                random.uniform(200, 1000),
                fake.date_between(start_date='-1y', end_date='today')
            )
            for _ in range(num_workouts)
        ]
        cur.executemany(
            "INSERT INTO Workouts (client_id, type, duration, calories_burned, session_date) VALUES (%s, %s, %s, %s, %s)", 
            workouts_data
        )
        conn.commit()
        print(f"Добавлено {num_clients} клиентов и {num_workouts} тренировок.")
    except mysql.connector.Error as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


def fetch_data():
    """Получает данные из таблицы Workouts."""
    try:
        conn = mysql.connector.connect(**DATABASE)
        cur = conn.cursor()
        
        
        cur.execute("""
            SELECT wc.workout_id, gc.name, gc.age, gc.gender, gc.membership_type, wc.type, wc.duration, wc.calories_burned, wc.session_date 
            FROM Workouts wc
            JOIN Gym_Clients gc ON wc.client_id = gc.client_id
        """)
        
        result = cur.fetchall()
        columns = ['workout_id', 'name', 'age', 'gender', 'membership_type', 'type', 'duration', 'calories_burned', 'session_date']
        data = pd.DataFrame(result, columns=columns)
        return data
    
    except mysql.connector.Error as e:
        print(f"Ошибка при получении данных: {e}")
        return pd.DataFrame()
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


def add_data(new_data):
    """Добавляет новые данные в таблицу Workouts."""
    try:
        conn = mysql.connector.connect(**DATABASE)
        cur = conn.cursor()
        
        
        for _, row in new_data.iterrows():
            cur.execute(
                "INSERT INTO Workouts (client_id, type, duration, calories_burned, session_date) VALUES (%s, %s, %s, %s, %s)",
                (row['client_id'], row['type'], row['duration'], row['calories_burned'], row['session_date'])
            )
        
        conn.commit()
        print(f"Добавлено {len(new_data)} новых записей в таблицу Workouts.")
    except mysql.connector.Error as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()


def delete_all_data():
    """Удаляет все данные из таблиц Workouts и Gym_Clients."""
    try:
        conn = mysql.connector.connect(**DATABASE)
        cur = conn.cursor()
        
        
        cur.execute("DELETE FROM Workouts")
        cur.execute("DELETE FROM Gym_Clients")
        conn.commit()
        print("Все данные были удалены.")
    except mysql.connector.Error as e:
        print(f"Ошибка при удалении данных: {e}")
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()
