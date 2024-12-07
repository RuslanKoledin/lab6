import os
from data_scraping import scrape_news
from text_preprocessing import summarize_and_analyze
from database import save_to_db

# Отключаем многозадачность для токенизаторов
os.environ["TOKENIZERS_PARALLELISM"] = "false"

if __name__ == "__main__":
    country = "us"  
    news = scrape_news(country)

    if news:
        for article in news:
            title = article['title']
            content = article.get('content')

            # Проверка, если в заголовке есть метка "REMOVE" или если контент слишком короткий
            if 'REMOVE' in title or content is None or len(content) < 10:
                print(f"Skipping article due to 'REMOVE' in title, insufficient content or None: {title}")
                continue

            # Создание резюме и прогноз тональности
            summary, sentiment = summarize_and_analyze(content)
            
            # Сохранение статьи в базу данных
            save_to_db(title, content, summary, sentiment)

            # Выводим результаты только если статья не помечена для удаления
            print("Title:", title)
            print("Summary:", summary)
            print("Sentiment:", sentiment)
            print("------")
    else:
        print("No news found.")
