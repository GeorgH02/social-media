from transformers import AutoModel, AutoTokenizer

print("Pre-downloading sentiment model files")
#lightweight sentiment analysis model (returns neutral, positive or negative)
model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
AutoModel.from_pretrained(model_name)
AutoTokenizer.from_pretrained(model_name)
print("Model files downloaded and cached successfully")
