import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from config import DATABASE
import mysql.connector

def fetch_data():
    """Извлекает данные для анализа."""
    try:
        conn = mysql.connector.connect(**DATABASE)
        query = "SELECT duration, calories_burned FROM Workouts"
        df = pd.read_sql(query, conn)
        conn.close()
        print(f"Извлечено {df.shape[0]} записей из базы данных.")
        return df
    except mysql.connector.Error as e:
        print(f"Ошибка при извлечении данных: {e}")
        return pd.DataFrame()
    

def analyze_and_visualize():
    """Анализирует данные и создает график."""
    data = fetch_data()
    if data.empty:
        print("Нет данных для анализа.")
        return

    # Подготовка данных
    X = data['duration'].values.reshape(-1, 1)
    y = data['calories_burned'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Обучение модели
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Метрики
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    print(f"MAE: {mae}, MSE: {mse}")

    # Визуализация
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
    plt.xlabel('Actual Calories Burned')
    plt.ylabel('Predicted Calories Burned')
    plt.title('Actual vs Predicted Calories Burned')
    plt.tight_layout()
    plt.show()
