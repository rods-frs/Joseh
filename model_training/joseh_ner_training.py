import spacy
from spacy.training import Example
import csv
import logging
import random
from collections import deque
from thinc.api import compounding
from os import system
from time import sleep

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("treinamento.log"),
        logging.StreamHandler()
    ]
)

#parameters
TRAINING_CSV = r"model_training/joseh_ner_training2.csv"
LABELS = [
    "program",
    "music"
]
patience = 10
DELTA = 0.01
interactions = 200
COMPOUND_SIZE = 1.01
BATCH_START_SIZE = 5
BATCH_END_SIZE = 25
MODEL_NAME = "joseh_ner_model_v2"

blank_nlp = spacy.blank("en")
ner = blank_nlp.add_pipe("ner")

for label in LABELS:
    ner.add_label(label)

def open_csv(path):
    with open(path, newline="") as f:
        print(f"Successfully readed: {path}")
        return list(csv.DictReader(f))

def find_word(text, word):
    start = text.find(word)
    end = start + len(word)
    return start, end

reader = open_csv(TRAINING_CSV)

training_data = []

for row in reader:
    phrase = row["phrase"]
    word = row["word"]
    label = row["label"]
    start, end = find_word(phrase, word)
    training_data.append((phrase, {"entities": [(start, end, label)]}))

logging.info("Starting model training, this can take a while.")
optimizer = blank_nlp.begin_training()
losses = {}

batch_size = compounding(start=BATCH_START_SIZE, stop=BATCH_END_SIZE, compound=COMPOUND_SIZE)

#training stock paramenters
last_loss = float("inf")
current_loss = float("inf")
first_epoch = True
loss_window = deque(maxlen=10)
smooth_loss = 0

for _ in range(interactions):
    if patience <= 0:
        if current_loss >= 1:
            logging.info("Patience limit reached but loss is bigger than 1. Adding 1 patience point...")
            patience += 1
        else:
            logging.info("Patience limit reached! Ending training...")
            break

    random.shuffle(training_data)
    last_smooth_loss = smooth_loss
    losses = {}

    for batch in spacy.util.minibatch(training_data, size=batch_size):
        examples = []
        for t, a in batch:
            doc = blank_nlp.make_doc(t)
            entities = []
            for start, end, label in a["entities"]:
                span = doc.char_span(start, end, label=label, alignment_mode="expand")
                entities.append(span)
            doc.ents = entities
            example = Example.from_dict(doc, a)
            examples.append(example)
        blank_nlp.update(examples, sgd=optimizer, losses=losses, drop=0.2)


    current_loss = losses["ner"]
    system("clear 2>/dev/null")

    loss_window.append(current_loss)
    smooth_loss = sum(loss_window) / len(loss_window)

    if first_epoch:
        logging.info(f"Loss: {current_loss:.4f} | Last: N/A | Patience: {patience}")
        first_epoch = False

    elif last_smooth_loss - smooth_loss < DELTA:
        patience -= 1
        logging.info(f"Loss: {current_loss:.4f} | Last: {last_smooth_loss:.4f} | Patience: {patience}")
        logging.info("Not enough difference between errors, -1 patience point")

    else:
        logging.info(f"Loss: {current_loss:.4f} | Last: {last_smooth_loss:.4f} | Patience: {patience}")

logging.info("Finished training")

while True:
    sleep(1)
    text = input("Enter a phrase: ")
    if text == "quit": break
    doc = blank_nlp(text)
    for ent in doc.ents:
        print(f"Recognized word: {ent.text} | Label: {ent.label_}")

input("Press ENTER to save the model")
blank_nlp.to_disk(MODEL_NAME)