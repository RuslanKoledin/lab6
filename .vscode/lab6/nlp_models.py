from transformers import pipeline

# NLP Модели
summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")

def summarize_text(content):
    return summarizer(content, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

def analyze_sentiment(text):
    return sentiment_analyzer(text)[0]['label']
