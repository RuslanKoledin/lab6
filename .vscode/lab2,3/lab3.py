import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

try:
    df = pd.read_csv('spo.csv') 
except FileNotFoundError:
    print("Ошибка: Файл не найден. Проверьте путь к файлу.")
except pd.errors.EmptyDataError:
    print("Ошибка: Файл пуст.")
    df = pd.DataFrame(columns=['spo_type', 'age', 'calories', 'gender'])
    

app = dash.Dash(__name__)


app.layout = html.Div([
    
    html.Div([
        dcc.Dropdown(
            id='workout-type-filter',
            options=[{'label': workout, 'value': workout} for workout in df['spo_type'].unique()],
            value=df['spo_type'].unique(),
            multi=True,
            placeholder="Выберите тип тренировки"
        )
    ]),

    #слайдер для возвраства 
    html.Div([
        dcc.RangeSlider(
            id='age-range-slider',
            min=df['age'].min() if not df.empty else 0,
            max=df['age'].max() if not df.empty else 100,
            value=[df['age'].min() if not df.empty else 0, df['age'].max() if not df.empty else 100],
            marks={i: str(i) for i in range(df['age'].min() if not df.empty else 0, df['age'].max() if not df.empty else 101, 5)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Div(id='age-range-output')
    ]),

    
    html.Div([
        dcc.Dropdown(
            id='gender-filter',
            options=[
                {'label': 'Мужской', 'value': 'М'},
                {'label': 'Женский', 'value': 'Ж'}
            ],
            value=None,
            placeholder="Выберите пол"
        )
    ]),

    dcc.Graph(id='age-histogram'),

    dcc.Graph(id='calories-histogram'),

    dcc.Graph(id='workout-type-pie')
])

@app.callback(
    [Output('age-histogram', 'figure'),
     Output('calories-histogram', 'figure'),
     Output('workout-type-pie', 'figure')],
    [Input('workout-type-filter', 'value'),
     Input('age-range-slider', 'value'),
     Input('gender-filter', 'value')]
)
def update_graphs(selected_workouts, selected_age_range, selected_gender):
    # фильтрация по типу тренировки, возрасту и полу
    filtered_df = df[df['spo_type'].isin(selected_workouts)]
    filtered_df = filtered_df[(filtered_df['age'] >= selected_age_range[0]) & (filtered_df['age'] <= selected_age_range[1])]

    if selected_gender:
        filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

    age_histogram = px.histogram(filtered_df, x='age', nbins=20, title='Распределение участников по возрасту')

    calories_histogram = px.histogram(filtered_df, x='calories', nbins=20, title='Распределение калорий на тренировку')

    workout_type_pie = px.pie(filtered_df, names='spo_type', title='Распределение тренировок по типам')

    return age_histogram, calories_histogram, workout_type_pie


if __name__ == '__main__':
    app.run_server(debug=True)
