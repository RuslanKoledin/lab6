import time
from db_operations import create_tables, generate_data
from ml_analysis import analyze_and_visualize

if __name__ == '__main__':
    while True:
        print("Обновление данных и выполнение анализа...")
        create_tables()
        generate_data()
        analyze_and_visualize()
        print("Данные обновлены. Ожидание 3 секунд...")
        time.sleep(3)
