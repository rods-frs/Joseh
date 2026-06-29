import spacy
import logging
import re
from core.error_handler import NLPError, InvalidCommand, NoNounDetected

nlp_logger = logging.getLogger("NLP")

def split_command(text):
    nlp_logger.debug(f"Splitting command: {text}")
    try:
        parts = re.split(r'\b(and then|and|also|then)\b|(\s*,\s*)', text, flags=re.IGNORECASE)
        clean_parts = []
        for p in parts:
            if p is None:
                continue
            p = p.strip()
            if p and p.lower() not in ('and', 'then', 'and then', 'also',',', ''):
                nlp_logger.debug(f"Adding part to clean_parts: {p}")
                clean_parts.append(p)
        return clean_parts
    except Exception as e:
        raise NLPError(f"Failed to split command: {e}")

def init_models(CAT_MODEL_PATH='/home/rodrigo/Joseh/tools/model/joseh_cat_model_v2', NER_MODEL_PATH='/home/rodrigo/Joseh/tools/model/joseh_ner_model_v2'):
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
        special_clauses = []
        for clause in clauses:
            doc = cat_model(clause)
            for intent, score in doc.cats.items():
                if score >=threshold:
                    nlp_logger.debug(f"Intent recognized: {intent}")
                    if intent == 'play_music': 
                        nlp_logger.debug(f"play_music command detected. adding the clause '{clause}' to special_clauses")
                        special_clauses.append(clause)
                    detected_commands.append(intent)
        if len(detected_commands) >= 1: return detected_commands, special_clauses
        else:
            raise InvalidCommand("No intent were recognized")
    except InvalidCommand:
        raise
    except Exception as e:
        raise NLPError(f"Failed to recognize the intention: {e}")

def detect_noun_name(text, expected_type):
    nlp_logger.debug(f"Detecting the noun in the phrase: {text}")
    detected_name = ""
    try:
        doc = ner_model(text)
        for ent in doc.ents:
            if ent.label_ != expected_type:
                nlp_logger.warning(f"Type recognized is different than expected. Expected: {expected_type} | Got: {ent.label_}")
                if IGNORE_TYPE_WARNING: 
                    detected_name = ent.text
                    return detected_name
            elif ent.label_ == expected_type:
                nlp_logger.debug("Type detected match the expected.")
                detected_name = ent.text
                return detected_name
            else:
                raise NLPError(f"Couldn`t detected the noun.")
        if not detected_name: 
            raise NoNounDetected(f"No nouns were detected in the phrase {text}")
    except Exception as e:
        raise NLPError(f"Failed to detect the noun: {e}")

def load_specific_model(model_name):
    if model_name == 'base':
        return base_model
    elif model_name == 'cat':
        return cat_model
    elif model_name == 'ner':
        return ner_model

def enable_ignore_type_warning_flag():
    nlp_logger.info("The flag 'ignore_type_warning' is active. ")
    global IGNORE_TYPE_WARNING
    IGNORE_TYPE_WARNING = True
