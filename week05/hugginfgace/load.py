from transformers import pipeline

classifier = pipeline("text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

result = classifier("I love learning Python!")
print(result)