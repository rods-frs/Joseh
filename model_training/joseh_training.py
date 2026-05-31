import spacy
import csv
import logging
import random
from spacy.training import Example
from os import system
from time import sleep
from collections import deque

#//

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("treinamento.log"),
        logging.StreamHandler()
    ]
)

#//

labels = [
    "resume",
    "pause",
    "skip",
    "next",
    "back",
    "previous",
    "update",
    "date"
]

#//

blank_nlp = spacy.blank("en")
textcat = blank_nlp.add_pipe("textcat_multilabel")
for label in labels:
    textcat.add_label(label)

#//

cat_training_data = []
TRAINING_CSV = "model_training/joseh_training_data2.csv"

def open_csv(path):
    with open(path, newline="") as f:
        print(f"Successfully readed: {path}")
        return list(csv.DictReader(f))

reader = open_csv(TRAINING_CSV)

for row in reader:
    phrase = row["phrase"]
    intent = row["intent"]
    logging.debug(f"Intent = {intent}")
    cats = {label: (1.0 if label == intent else 0.0) for label in labels}
    cat_training_data.append((phrase, {"cats": cats}))

#//
input("Press ENTER to continue")
for row in cat_training_data[:5]:
    logging.debug(row)

interactions = 200
logging.info("Starting model training, this can take a while.")
optimizer = blank_nlp.begin_training()
losses = {}

patience = 10
last_loss = float("inf")
current_loss = float("inf")
first_epoch = True
loss_window = deque(maxlen=10)
DELTA = 0.01


for _ in range(interactions):
    if patience <= 0:
        if current_loss >= 1:
            logging.info("Patience limit reached but loss is bigger than 1. Adding 1 patience point...")
            patience += 1
        else:
            logging.info("Patience limit reached! Ending training...")
            break

    random.shuffle(cat_training_data)
    last_smooth_loss = smooth_loss
    losses = {}

    for text, annotations in cat_training_data:
        doc = blank_nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        blank_nlp.update([example], sgd=optimizer, losses=losses, drop=0.2)

    current_loss = losses["textcat_multilabel"]
    system("clear 2>/dev/null")

    loss_window.append(current_loss)
    smooth_loss = sum(loss_window) / len(loss_window)

    if first_epoch:
        logging.info(f"Loss: {current_loss:.4f} | Last: N/A | Patience: {patience}")
        first_epoch = False

    elif last_smooth_loss - smooth_loss < DELTA:
        patience -= 1
        logging.info(f"Loss: {current_loss:.4f} | Last: {last_loss:.4f} | Patience: {patience}")
        logging.info("Not enough difference between errors, -1 patience point")

    else:
        logging.info(f"Loss: {current_loss:.4f} | Last: {last_loss:.4f} | Patience: {patience}")

logging.info("Finished training")
while True:
    sleep(1)
    text = input("Enter a phrase: ")
    if text == "quit": break
    doc = blank_nlp(text)
    for label, score in doc.cats.items():
        logging.info(f"{label}: {score:.4f}")

input("Press ENTER to save the model")
blank_nlp.to_disk("joseh_model_v1")

