#import recognizer
#mic, stream = recognizer.create_mic()
#model = recognizer.load_model("/home/rodrigo/Joseh/tools/stt/vosk-model-en-us-0.22")
#recognizer.wake_word_detection(model, stream, "michael")
#result = recognizer.get_user_command(model, stream)
#print(result)

MODEL_PATH = "/home/rodrigo/Joseh/tools/stt/vosk-model-en-us-0.22"

import json
import audioop
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import queue

INPUT_RATE = 48000
VOSK_RATE = 16000
CHUNK = 8192
SILENCE_THRESHOLD = 10000000  # adjust this if needed

#model = Model(MODEL_PATH)
#recognizer = KaldiRecognizer(model, VOSK_RATE)

audio_queue = queue.Queue()
resample_state = None

def callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))

print("Available devices:")
print(sd.query_devices())
print(f"\nDefault input: {sd.query_devices(kind='input')['name']}")
print("\nListening... (Ctrl+C to stop)")

with sd.RawInputStream(samplerate=INPUT_RATE, channels=1, dtype="int16", blocksize=CHUNK, callback=callback, device=10):
    while True:
        data = audio_queue.get()

        volume = audioop.rms(data, 2)
        print(f"Volume: {volume}", end="\r")  # watch this while speaking

        if volume < SILENCE_THRESHOLD:
            continue  # skip silent chunks entirely
