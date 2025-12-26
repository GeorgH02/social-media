from transformers import pipeline
import torch

_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    top_k=None,)

def classify_text(text: str):
    """Return the raw pipeline result for `text`.

    Keeps pipeline initialization at module level so imports are cheap.
    """
    if not text:
        return {"error": "No text provided"}
    return _sentiment_classifier(text)






