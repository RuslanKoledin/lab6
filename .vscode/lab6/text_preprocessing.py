from transformers import pipeline

# Загружаем модели
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
sentiment_analyzer = pipeline("sentiment-analysis")

def summarize_and_analyze(content):
    if not content or len(content) < 10:
        return "Content too short to summarize", "NEUTRAL"

    # Резюмирование
    summary = summarizer(content, max_length=50, min_length=25, do_sample=False)
    summary_text = summary[0]['summary_text']

    # Анализ тональности
    sentiment = sentiment_analyzer(summary_text)[0]
    sentiment_label = sentiment['label']  # "POSITIVE" или "NEGATIVE"
    
    return summary_text, sentiment_label

