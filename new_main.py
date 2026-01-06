#imports
import functions
import spacy

#global variables

#spacy preparation
nlp = spacy.load("en_core_web_sm")

#main logic
doc = nlp(str(input(">> ")))

verb = functions.get_verb(doc)
print(f"Verb found: {verb}")

if verb.lemma_ == "open":

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