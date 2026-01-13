#imports
import spacy
from nlp_training import get_intent
from os import system
import functions

#spacy preparation
sysup_nlp = spacy.load("sys_up_model")
reqdate_nlp = spacy.load("req_date_model")

#main logic

program_break = False

while not program_break:
    usr_input = str(input(">> "))

    if usr_input == "exit":
        program_break = True

    sys_up_intent = get_intent("update_system", sysup_nlp, usr_input)
    req_date_intent = get_intent("request_date", reqdate_nlp, usr_input)

    if sys_up_intent:
        q_usr_sysup = str(input("System update function trigger!\nProceed?\n>> ")).lower()
        print(q_usr_sysup)
        if q_usr_sysup == "yes":
            functions.update_sys()
        else:
            print("User command to update the system was interupted")

    elif req_date_intent:
        print("Request date function trigger!")
        system("date")