#!/usr/bin/env python3
"""Pre-download the sentiment model during Docker build to cache it."""

from transformers import pipeline

print("Pre-downloading sentiment model...")
pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    top_k=None,
)
print("Model downloaded and cached successfully!")
