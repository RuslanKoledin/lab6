import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score, precision_score, recall_score
from config import DATABASE
import mysql.connector

# Функция для извлечения данных из базы
def fetch_data():
    """Извлекает данные для анализа."""
    try:
        conn = mysql.connector.connect(**DATABASE)
        query = "SELECT duration, calories_burned FROM Workouts"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as e:
        print(f"Ошибка при извлечении данных: {e}")
        return pd.DataFrame()

# Функция анализа данных
def analyze_data():
    """Анализирует данные и возвращает метрики и данные для графика."""
    data = fetch_data()
    if data.empty:
        return None, None, None

    X = data['duration'].values.reshape(-1, 1)
    y = data['calories_burned'].values

    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Обучение модели
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Метрики регрессии
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)

    # Данные для графика
    results = {
        "y_test": y_test,
        "predictions": predictions
    }
    return mae, mse, results

# Создание Dash приложения
app = dash.Dash(__name__)

# Layout Dash приложения
app.layout = html.Div([
    html.H1("Динамическая визуализация анализа данных", style={"textAlign": "center"}),
    html.Div([
        html.P(id="mae-display", style={"textAlign": "center", "fontSize": "18px"}),
        html.P(id="mse-display", style={"textAlign": "center", "fontSize": "18px"})
    ]),
    dcc.Graph(id="dynamic-graph"),
    dcc.Interval(
        id="interval-component",
        interval=3000,  
        n_intervals=0  # Счетчик интервалов
    )
])

# Обновление данных и графика
@app.callback(
    [dash.dependencies.Output("dynamic-graph", "figure"),
     dash.dependencies.Output("mae-display", "children"),
     dash.dependencies.Output("mse-display", "children")],
    [dash.dependencies.Input("interval-component", "n_intervals")]
)
def update_graph(n):
    mae, mse, results = analyze_data()
    if results:
        y_test = results["y_test"]
        predictions = results["predictions"]

        # График: Фактические значения vs Предсказания
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y_test, y=predictions, mode='markers',
            marker=dict(size=8, opacity=0.6),
            name="Predictions"
        ))
        fig.add_trace(go.Scatter(
            x=[y_test.min(), y_test.max()],
            y=[y_test.min(), y_test.max()],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name="Ideal Line"
        ))

        # Обновление масштаба и осей
        fig.update_layout(
            title="Actual vs Predicted Calories Burned",
            xaxis_title="Actual Calories Burned",
            yaxis_title="Predicted Calories Burned",
            xaxis=dict(
                range=[y_test.min() - 10, y_test.max() + 10]  # Устанавливаем диапазон оси X с отступом
            ),
            yaxis=dict(
                range=[min(predictions) - 10, max(predictions) + 10]  # Устанавливаем диапазон оси Y с отступом
            ),
            template="plotly_white"
        )

        mae_text = f"Mean Absolute Error (MAE): {mae:.2f}"
        mse_text = f"Mean Squared Error (MSE): {mse:.2f}"
    else:
        fig = go.Figure()
        fig.update_layout(title="No Data Available")
        mae_text = "No MAE available"
        mse_text = "No MSE available"

    return fig, mae_text, mse_text

# Запуск Dash сервера
if __name__ == "__main__":
    app.run_server(debug=True)
