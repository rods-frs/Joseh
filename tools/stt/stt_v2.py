import json
import pyaudio
import logging
#import audioop
import numpy as np
from openwakeword.model import Model
from faster_whisper import WhisperModel

#configure logging
global sst_logger
sst_logger = logging.getLogger("STT")

def load_model_and_variables(wake_word):
    try:
        global stt_model, wakeword_model, wakeword, format, channels, rate, chunk
        wakeword = wake_word
        format=pyaudio.paInt16
        channels=1
        rate=16000
        chunk=1280

        sst_logger.debug("Loading STT and WW model")
        stt_model = WhisperModel("tiny", device="cpu", compute_type="int8")
        wakeword_model = Model(wakeword_models=[wake_word])

        sst_logger.debug("Done!")
    except Exception as e:
        sst_logger.error(f"Failed to load the STT models: {e}")

def create_mic():
    try:
        sst_logger.debug("Creating mic and stream")
        mic = pyaudio.PyAudio()
        stream = mic.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
        sst_logger.debug("Done! Returning stream to main")
        return mic, stream
    except Exception as e:
        sst_logger.error(f"Error while creating virtual mic: {e}")

def wake_word_detection(stream, chunk=1280, channels=1):
    try:
        while True:
            audio_data = stream.read(chunk, exception_on_overflow=False)
            audio_frame = np.frombuffer(audio_data, dtype=np.int16)
            prediction = wakeword_model.predict(audio_frame)
            if prediction[wakeword] > 0.5:
                stt_model.info("Wake word detected!")
                break
    except Exception as e:
        pass

def get_user_command(model, stream):
    try:
        # Stop the wake-word listener briefly to record the user's command
        stt_model.info("Listening to your command...")
        recording_frames = []
        
        # Record a fixed window (e.g., 4 seconds) or implement silence detection
        for _ in range(0, int(rate / chunk * 4)):
            data = stream.read(chunk, exception_on_overflow=False)
            recording_frames.append(data)

        raw_audio_speech = b"".join(recording_frames)
        
        speech_array = np.frombuffer(raw_audio_speech, dtype=np.int16).astype(np.float32) / 32768.0
        
        segments, info = stt_model.transcribe(speech_array, beam_size=5)
    except Exception as e:
        print(f"Failed to get the user command: {e}")

if __name__ == "__main__":
    model = load_model("/home/rodrigo/Joseh/tools/stt/vosk-model-en-us-0.22")
    mic, stream = create_mic()
    wake_word_detection(model, stream, "michael")
    user_command = get_user_command(model, stream)
    print(user_command)