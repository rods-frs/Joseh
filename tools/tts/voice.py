import pyttsx3
import logging

global tts_logger
tts_logger = logging.getLogger("TTS")

global joseh_muted
joseh_muted = False

class TTSError(Exception):
    def __init__(self, message):
        tts_logger.error(message)
        super().__init__(message)

def tts_configuration(rate=150):
    tts_logger.debug("Starting the TTS module")
    try:
        global engine
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
    except Exception as e:
        raise TTSError(f"Failed to start the TTS module: {e}")

def mute_joseh():
    tts_logger.warning("mute_joseh flag is active!")
    global joseh_muted
    joseh_muted = True

def talk_and_print(text):
    if not joseh_muted:
        engine.say(text)
        engine.runAndWait
    print(text)
