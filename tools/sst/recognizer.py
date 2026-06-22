from vosk import Model, KaldiRecognizer
import json
import pyaudio
import logging

#configure logging
global sst_logger
sst_logger = logging.getLogger("SST")

def load_model(model_path):
    try:
        sst_logger.debug("Loading model")
        model = Model(model_path)
        sst_logger.debug("Done! Returning model to main")
        return model
    except Exception as e:
        sst_logger.error(f"Failed to load the model at {model_path}: {e}")

def create_mic():
    try:
        sst_logger.debug("Creating mic and stream")
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
        sst_logger.debug("Done! Returning stream to main")
        return stream
    except Exception as e:
        sst_logger.error(f"Error while creating virtual mic: {e}")

def wake_word_detection(model, stream, wake_word):
    try:
        sst_logger.debug("Creating recording object")
        wake_rec = KaldiRecognizer(model, 16000, f'[{wake_word}]')
        wake_word_heard = None
        sst_logger.info(f"Waiting for the wake word: {wake_word}")
        while wake_word_heard is None:
            data = stream.read(4000, exception_on_overflow=False)
            if wake_rec.AcceptWaveform(data):
                sst_logger.info("Wake-word detected! Checking word")
                result = json.loads(wake_rec.Result())
                if wake_word in result.get("text", ""):
                    logging.info("Wake word confirmed!")
                    wake_word_heard = True
                else:
                    sst_logger.warning(f"Wake word was not confirmed, please check. Word detected: {result.get("text", "")}")
        return wake_word_heard
    except Exception as e:
        sst_logger.error(f"Failed to wait for the wake word: {e}")

def get_user_command(model, stream):
    try:
        command_rec = KaldiRecognizer(model, 16000)
        user_command = None
        while user_command is None:
            print("Phase 4")
            data = stream.read(4000, exception_on_overflow=False)
            print("phase 5")
            if command_rec.AcceptWaveform(data):
                result = json.loads(command_rec.Result())
                print("Phase 6")
                if result.get("text"):
                    user_command = result["text"]
        return user_command
    except Exception as e:
        print(f"Failed to get the user command: {e}")

if __name__ == "__main__":
    model = load_model("/home/rodrigo/Documents/GitHub/Joseh/vosk-model-en-us-0.22")
    stream = create_mic()
    wake_word_detection(model, stream, "michael")
    user_command = get_user_command(model, stream)
    print(user_command)