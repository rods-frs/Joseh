#not flexible for now -> Just for "update system"

#imports
import spacy
import random
from spacy.training import Example
from os import system

def create_model():
    nlp = spacy.blank("en")
    textcat = nlp.add_pipe("textcat")
    textcat.add_label("update_request")
    textcat.add_label("not_update_request")

    return nlp

def training_data():
    return [
        ("Update the system", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("I need a system upgrade", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Please install updates", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("System requires update", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Check for system updates", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Install the latest version", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Upgrade my current system", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Need to update software", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("System update required", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Download and install updates", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Apply system patches", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Update all system components", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Perform system upgrade", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("I want to refresh my system", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Check for available updates", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("System needs updating", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Install pending updates", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Update my operating system", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Perform software maintenance", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Upgrade system software", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Run system update process", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("I want to update now", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("System update is necessary", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Initiate system upgrade", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Update all software", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("We need to update the system", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Time to get the latest updates", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Let's update the software", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("Update required for this system", {"cats": {"update_request": 1.0, "not_update_request": 0.0}}),
        ("What's the time?", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Open my email", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Show me the weather", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Play some music", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Call my friend", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Set a reminder", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("What's on my calendar?", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Search the internet", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Take a note", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Calculate something", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Open a website", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Send a message", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Check my bank account", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Order food", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Book a ride", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Find a restaurant", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Get directions", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Check flight status", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Read news", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Listen to a podcast", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Start a timer", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Convert currency", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Check stock prices", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Translate a phrase", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Create a playlist", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Find a recipe", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Check movie times", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Look up a definition", {"cats": {"update_request": 0.0, "not_update_request": 1.0}}),
        ("Start a video call", {"cats": {"update_request": 0.0, "not_update_request": 1.0}})
    ]

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

def get_intent(nlp, text):
    doc = nlp(text)
    update_prob = doc.cats["update_request"]
    return update_prob > 0.5


#test / base syntax

if __name__ == "__main__":

    nlp = create_model()
    train_data = training_data()
    new_nlp = train_model(nlp, train_data)

    text_1 = input("Whats the command?")
    text_2 = input("Whats the other command?")

    intent1 = get_intent(new_nlp, text_1)
    intent2 = get_intent(new_nlp, text_2)

    print(f"{intent1}, {intent2}")


