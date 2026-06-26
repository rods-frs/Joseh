import spacy
import logging
from tools.toolbox import split_command

global nlp_logger
nlp_logger = logging.getLogger("NLP")

class NLPError(Exception):
    def __init__(self, message):
        nlp_logger.error(message)
        super().__init__(message)

def init_models(CAT_MODEL_PATH='joseh_cat_model_v2', NER_MODEL_PATH='joseh_ner_model_v2'):
    nlp_logger.debug("Starting init of the NLP models")
    try:
        global base_model
        global cat_model 
        global ner_model 
        base_model = spacy.load('en_core_web_lg')
        cat_model = spacy.load(CAT_MODEL_PATH)
        ner_model = spacy.load(NER_MODEL_PATH)
        nlp_logger.debug("All models initialized!")
    except Exception as e:
        raise NLPError(f"Failed to start the models: {e}")

def detect_intent(text, threshold=0.5):
    nlp_logger.debug(f"Detecting intent of the phrase: {text}")
    try:
        clauses = split_command(text)
        detected_commands = []
        for clause in clauses:
            doc = cat_model(clause)
            for intent, score in doc.cats.items():
                if score >=threshold:
                    nlp_logger.debug(f"Intent recognized: {intent}")
                    detected_commands.append(intent)
        if len(detected_commands) >= 1: return detected_commands
        else:
            raise NLPError("No intent were recognized")
    except Exception as e:
        raise NLPError(f"Failed to recognize the intention: {e}")
    
def detect_noun_name(text, expected_type, IGNORE_TYPE_WARNING=True):
    nlp_logger.debug(f"Detecting the noun in the phrase: {text}")
    detected_name = ""
    try:
        doc = ner_model(text)
        for ent in doc.ents:
            if ent.label_ != expected_type:
                nlp_logger.warning(f"Type recognized is different than expected: {ent.label_}")
                if IGNORE_TYPE_WARNING: 
                    detected_name = ent.text
                    return detected_name
            elif ent.label_ == expected_type:
                nlp_logger.debug("Type detected match the expected.")
                detected_name = ent.text
                return detected_name
            else:
                raise NLPError(f"Couldn`t detected the noun.")
    except Exception as e:
        raise NLPError(f"Failed to detect the noun: {e}")

    