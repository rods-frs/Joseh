import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)

def talk_and_print(text):
    engine.say(text)
    engine.runAndWait()
    print(text)

talk_and_print("Hello")