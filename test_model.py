import spacy
from time import sleep

model = spacy.load('joseh_ner_model_v1')

while True:
    sleep(1)
    text = input("Enter a phrase: ")
    if text == "quit": break
    doc = model(text)
    for ent in doc.ents:
        print(f"Recognized word: {ent.text} | Label: {ent.label_}")