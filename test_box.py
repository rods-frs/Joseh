import json
import pyaudio
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-en-us-0.22") #loads the module

wake_rec = KaldiRecognizer(model, 16000, '["michael"]') #
command_rec = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

wake_word_heard = None
user_command = None

# stage 1: wait for the wake word
while wake_word_heard is None:
    print("Phase 1")
    data = stream.read(4000, exception_on_overflow=False)
    print("Phase 2")
    if wake_rec.AcceptWaveform(data):
        print("Phase 3")
        result = json.loads(wake_rec.Result())
        if "michael" in result.get("text", ""):
            print("Got it!")
            wake_word_heard = result["text"]
        else:
            print(f"Nah uh: {result.get("text", "")}")

# stage 2: capture the actual command
while user_command is None:
    print("Phase 4")
    data = stream.read(4000, exception_on_overflow=False)
    print("phase 5")
    if command_rec.AcceptWaveform(data):
        result = json.loads(command_rec.Result())
        print("Phase 6")
        if result.get("text"):
            user_command = result["text"]

print(wake_word_heard, user_command)