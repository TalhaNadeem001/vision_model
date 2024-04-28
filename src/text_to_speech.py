import pyttsx3

def text_to_speech(text):
    speech = pyttsx3.init()
    speech.say(text)
    speech.runAndWait()
