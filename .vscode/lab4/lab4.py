import json
import random
from datetime import datetime, timedelta
from faker import Faker
import mysql.connector


with open("/Users/ruslan/Documents/DataScience/.vscode/lab4/configDB.json") as config_file:
    config = json.load(config_file)


db = mysql.connector.connect(
    host=config["DB_HOST"],
    user=config["DB_USER"],
    password=config["DB_PASSWORD"],
    database=config["DB_NAME"]
)
cursor = db.cursor()

fake = Faker()
Faker.seed(42)

genders = ["Male", "Female", "Other"]
membership_types = ["Basic", "Premium", "VIP"]

for _ in range(100):
    name = fake.first_name()
    age = random.randint(18, 65)
    gender = random.choice(genders)
    membership_type = random.choice(membership_types)

    cursor.execute("INSERT INTO Gym_Clients (name, age, gender, membership_type) VALUES (%s, %s, %s, %s)",
                   (name, age, gender, membership_type))
db.commit()

# Получаем идентификаторы клиентов для привязки к тренировкам
cursor.execute("SELECT client_id FROM Gym_Clients")
client_ids = [row[0] for row in cursor.fetchall()]

# Список типов тренировок
workout_types = ["Cardio", "Strength", "Yoga", "HIIT", "Pilates"]

# Создание 50 случайных тренировок для клиентов
for _ in range(50):
    client_id = random.choice(client_ids)
    workout_type = random.choice(workout_types)
    duration = random.randint(30, 90)  # Длительность в минутах
    calories_burned = random.randint(200, 700)
    session_date = datetime.now() - timedelta(days=random.randint(0, 365))

    cursor.execute("INSERT INTO Workouts (client_id, type, duration, calories_burned, session_date) VALUES (%s, %s, %s, %s, %s)",
                   (client_id, workout_type, duration, calories_burned, session_date.date()))
db.commit()

print("100 уникальных клиентов и 50 тренировок добавлены в базу данных.")
cursor.close()
db.close()
