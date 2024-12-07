import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# чтение данных из файла csv 
df = pd.read_csv('spo.csv')

# среднее значение возвраста спортсменов 
avg_age = df['age'].mean()

# среднее значение сожженныз каллорий спортсменов 
avg_calories = df['calories'].mean()

# медиана возвраста спортсменов 
median_age= df['age'].median()

# мода возвраста спортсменов 
mode_spo_type = df['spo_type'].mode()[0]

# стандартное отклонение каллорий 
std_calories = df['calories'].std()

# вывод всех результатов 
print("\nВыводы:")
print(f"Средний возвраст спортсменов : {avg_age}.")
print(f"Среднее значение сожженных каллорий :{avg_calories}")
print(f"Медиана (срединное значение): {median_age}.")
print(f"Мода (наиболее часто встречающийся вид спорта): {mode_spo_type}.")
print(f"Стандартное отклонение (измеряет разброс данных): {std_calories:.2f}.")

# настройка стилей графиков
sns.set(style='whitegrid')

# гистограмма распределения возраста
plt.figure(figsize=(12, 5))

# построение гистограммы возраста
plt.subplot(1, 2, 1)
plt.hist(df['age'], bins=10, color='skyblue', edgecolor='black')
plt.title('Распределение возраста')
plt.xlabel('Возраст')
plt.ylabel('Частота')

# нистограмма распределения калорий
plt.subplot(1, 2, 2)
plt.hist(df['calories'], bins=10, color='lightgreen', edgecolor='black')
plt.title('Распределение калорий')
plt.xlabel('Калории')
plt.ylabel('Частота')

# отображение гистограмм
plt.tight_layout()
plt.show()

# диаграмма распределения тренировок по типам
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='spo_type', palette='viridis')

# настройка диаграммы
plt.title('Распределение тренировок по типам')
plt.xlabel('Тип тренировки')
plt.ylabel('Частота')
plt.xticks(rotation=45)

# отображение диаграммы
plt.tight_layout()
plt.show()
