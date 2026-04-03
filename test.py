import spacy

ner_nlp = spacy.load("NER_MODEL")
doc = ner_nlp("play the playlist 80s Rock")
print([(ent.text, ent.label_) for ent in doc.ents])