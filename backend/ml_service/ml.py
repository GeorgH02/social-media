from transformers import pipeline
import torch

_sentiment_classifier = None

def classify_text(text: str):
    global _sentiment_classifier
    if not text:
        return {"error": "No text provided"}
    #only initialzing model if initialization during build time failed
    if _sentiment_classifier is None:
        _sentiment_classifier = pipeline(
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
            top_k=None,
        )
    return _sentiment_classifier(text)






