#Now Flexible!

#imports
import spacy
from spacy.training import Example
import random
from os import system
import csv

def open_t_data_csv(csv_path):
    with open(csv_path, newline="") as f: 
        return list(csv.DictReader(f))

def create_model(it, n_it):
    nlp = spacy.blank("en")
    textcat = nlp.add_pipe("textcat")
    textcat.add_label(it)
    textcat.add_label(n_it)

    return nlp

def training_data(it1, n_it1, reader):

    training_data_v = []

    for row in reader:
        phrase = row["phrase"]
        score = row["score"]
        if score == "0":
            training_data_v.append((phrase, {"cats": {it1: 0.0, n_it1: 1.0}}))
        else:
            training_data_v.append((phrase, {"cats": {it1: 1.0, n_it1: 0.0}}))

    return training_data_v

def train_model(nlp, training_data, interations=150):
    optimizer = nlp.begin_training()
    losses = {}
    n_inter = 1
    fix_perc = 100 / interations
    perc = 0
    for _ in range(interations):
        random.shuffle(training_data)
        for text , annotations in training_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer, losses=losses)
        system("clear")
        int_perc = int(perc)
        print(f"NLP training {int_perc}% completed")
        perc += fix_perc
    print("Training completed!")
    return nlp

def get_intent(it, nlp, text):
    doc = nlp(text)
    it_prob = doc.cats[it]
    return it_prob > 0.5

def main(path, it, n_it, test_p1, test_p2, model_name):
    nlp = create_model(it, n_it)
    t_csv = open_t_data_csv(path)
    train_data = training_data(it, n_it,t_csv)
    new_nlp = train_model(nlp, train_data)

    true_intent = get_intent(it, new_nlp, test_p1)
    false_intent = get_intent(it, new_nlp, test_p2)

    if true_intent == True and false_intent == False:
        print("NLP test: PASSED")
        import_model = int(input("Import model?\n1- Yes\nEverything else - No\n>> "))
        if import_model == 1: 
            new_nlp.to_disk(model_name) 
        else: 
            print("Model not exported")
    else:
        print("NLP test: FAILED")
    
#test / base syntax

if __name__ == "__main__":
    main("/home/morsdesuper/Documents/joseh/Joseh/update_t_data.csv", "update_system", "n_update_system", "please update my system", "whats the weather today?")