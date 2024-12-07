import json
import mysql.connector
from mysql.connector import Error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import plot_tree

try:
    with open("/Users/ruslan/Documents/DataScience/.vscode/lab4/configDB.json") as config_file:
        config = json.load(config_file)
except FileNotFoundError as e:
    print(f"Ошибка: не удалось найти файл конфигурации. {e}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Ошибка: некорректный формат JSON в файле конфигурации. {e}")
    exit(1)

# Подключение к базе данных с обработкой исключений
try:
    db = mysql.connector.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"]
    )
    cursor = db.cursor()

    # Загрузка данных из таблиц
    workouts_query = "SELECT * FROM Workouts"
    workouts_df = pd.read_sql(workouts_query, db)

    clients_query = "SELECT * FROM Gym_Clients"
    clients_df = pd.read_sql(clients_query, db)

    # Объединение данных
    data = pd.merge(workouts_df, clients_df, on="client_id")

    # Преобразование категориальных данных
    data['gender'] = data['gender'].map({'Male': 0, 'Female': 1})
    data['membership_type'] = data['membership_type'].map({'Basic': 0, 'Premium': 1})

    X = data[['age', 'gender', 'membership_type']]
    y = data['type']

    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Создание и обучение модели
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Предсказание
    y_pred = model.predict(X_test)

    # Оценка модели
    conf_matrix = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(10, 7))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', 
                xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title('Матрица ошибок')
    plt.xlabel('Предсказанные классы')
    plt.ylabel('Истинные классы')
    plt.savefig("confusion_matrix.png") 
    plt.show()

    # Генерация отчета по классификации
    report = classification_report(y_test, y_pred, output_dict=True)

    report_df = pd.DataFrame(report).transpose()
    plt.figure(figsize=(10, 5))
    sns.heatmap(report_df.iloc[:-1, :3], annot=True, cmap='Blues', fmt='.2f', linewidths=.5)
    plt.title('Отчет по классификации')
    plt.xlabel('Метрики')
    plt.ylabel('Классы')
    plt.savefig("classification_report.png")  
    plt.show()

    # Визуализация дерева решений
    plt.figure(figsize=(12, 8))
    plot_tree(model, filled=True, feature_names=X.columns, class_names=model.classes_)
    plt.title("Дерево решений для классификации типа тренировки")
    plt.savefig("tree_decision.png") 
    plt.show()

except Error as e:
    print(f"Ошибка при работе с базой данных: {e}")

finally:
    if db.is_connected():
        cursor.close()
        db.close()
        print("Соединение с базой данных закрыто.")
