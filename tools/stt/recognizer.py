from vosk import Model, KaldiRecognizer
import json
import pyaudio
import logging
import audioop

#configure logging
global sst_logger
sst_logger = logging.getLogger("STT")

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
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=4000)
        sst_logger.debug("Done! Returning stream to main")
        return mic, stream
    except Exception as e:
        sst_logger.error(f"Error while creating virtual mic: {e}")

def wake_word_detection(model, stream, wake_word):
    try:
        sst_logger.debug("Creating recording object")
        wake_rec = KaldiRecognizer(model, 16000, f'["{wake_word}", "[unk]"]')
        wake_word_heard = None
        sst_logger.info(f"Waiting for the wake word: {wake_word}")
        while wake_word_heard is None:
            data = stream.read(4000, exception_on_overflow=False)
            data_resampled = audioop.ratecv(data, 2, 1, 44100, 16000, None)[0]
            if wake_rec.AcceptWaveform(data_resampled):
                sst_logger.info("Wake-word detected! Checking word")
                result = json.loads(wake_rec.Result())
                final_result = result.get("text", "")
                if wake_word in final_result:
                    logging.info("Wake word confirmed!")
                    wake_word_heard = True
                else:
                    sst_logger.warning(f"Wake word was not confirmed, please check. Word detected: {final_result}")
        return wake_word_heard
    except Exception as e:
        sst_logger.error(f"Failed to wait for the wake word: {e}")

def get_user_command(model, stream):
    try:
        command_rec = KaldiRecognizer(model, 16000)
        user_command = None
        while user_command is None:
            print("///////")
            data = stream.read(4000, exception_on_overflow=False)
            data_resampled = audioop.ratecv(data, 2, 1, 44100, 16000, None)[0]
            print("444444444")
            if command_rec.AcceptWaveform(data_resampled):
                result = json.loads(command_rec.Result())
                print("XXXXXXXXX")
                if result.get("text"):
                    user_command = result["text"]
        return user_command
    except Exception as e:
        print(f"Failed to get the user command: {e}")

if __name__ == "__main__":
    model = load_model("/home/rodrigo/Joseh/tools/stt/vosk-model-en-us-0.22")
    mic, stream = create_mic()
    wake_word_detection(model, stream, "michael")
    user_command = get_user_command(model, stream)
    print(user_command)