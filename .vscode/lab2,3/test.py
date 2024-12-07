import random
import pandas as pd
from faker import Faker

# Инициализация генератора фейковых данных
fake = Faker()
Faker.seed(42)

# Параметры для генерации данных
num_athletes = 100
genders = ['Male', 'Female']
membership_types = ['Basic', 'Premium']

# Список спортсменов
athletes_data = []

for _ in range(num_athletes):
    athlete = {
        "name": fake.first_name(),
        "age": random.randint(18, 40),
        "gender": random.choice(genders),
        "membership_type": random.choice(membership_types),
    }
    athletes_data.append(athlete)

# Создаем DataFrame
athletes_df = pd.DataFrame(athletes_data)

# Сохраняем данные в CSV для дальнейшего использования
athletes_df.to_csv("test.csv", index=False)

# Выводим несколько строк для проверки
print(athletes_df.head())
