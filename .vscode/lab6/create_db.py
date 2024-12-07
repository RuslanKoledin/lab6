import mysql.connector
from config import DATABASE

def create_database():
    # Подключение к серверу MySQL
    db = mysql.connector.connect(
        host=DATABASE['host'],
        user=DATABASE['user'],
        password=DATABASE['password']
    )
    cursor = db.cursor()
    
    # Создание базы данных
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE['database']}")
    db.database = DATABASE['database']

    # Создание таблицы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            summary TEXT,
            sentiment VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.close()
    print("Database and table created successfully!")

if __name__ == "__main__":
    create_database()
