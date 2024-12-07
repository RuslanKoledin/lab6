import mysql.connector
from config import DATABASE

def connect_db():
    
    return mysql.connector.connect(
        host=DATABASE['host'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        database=DATABASE['database']
    )

def save_to_db(title, content, summary, sentiment):
    db = connect_db()
    cursor = db.cursor()
    query = """
        INSERT INTO news_articles (title, content, summary, sentiment)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (title, content, summary, sentiment))
    db.commit()
    cursor.close()
    db.close()
    print(f"Saved article '{title}' to the database.")
