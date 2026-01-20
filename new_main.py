#imports
<<<<<<< Updated upstream
=======
import spacy
from os import system
>>>>>>> Stashed changes
import functions
import spacy

#global variables

#spacy preparation
<<<<<<< Updated upstream
nlp = spacy.load("en_core_web_sm")
=======
sysup_nlp = spacy.load("sys_up_model")
reqdate_nlp = spacy.load("req_date_model")
openprog_nlp = spacy.load("get_program_name_model")
openprog_int_nlp = spacy.load("open_program_model")
>>>>>>> Stashed changes

#main logic
doc = nlp(str(input(">> ")))

verb = functions.get_verb(doc)
print(f"Verb found: {verb}")

if verb.lemma_ == "open":

<<<<<<< Updated upstream
    print("Function OPEN triggered")
    ap = functions.get_obj(doc)
    ap = str(ap).lower()
    print(f"Application name: {ap}")
    p_path = functions.get_p_path(ap)
    if p_path:
        p_path = p_path.split()[0]
        print(f"Path found: {p_path}")
        functions.open_p(p_path)
    else:
        print(f"{ap} was not found")
=======
    if usr_input == "exit":
        program_break = True

    sys_up_intent = get_intent("update_system", sysup_nlp, usr_input)
    req_date_intent = get_intent("request_date", reqdate_nlp, usr_input)
    open_program_intent = get_intent("open_program", openprog_int_nlp, usr_input)


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
    
    elif open_program_intent:
        doc = openprog_nlp(usr_input)
        first_object = True
        for ent in doc.ents:
            if first_object:
                p_name = ent.text
                print(p_name)
                first_object = False
            else:
                print(f"Extra object detected: {ent.text}")
        
        p_path = functions.get_p_path(p_name)
        functions.open_p(p_path)
>>>>>>> Stashed changes
