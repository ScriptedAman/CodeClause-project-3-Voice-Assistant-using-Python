import speech_recognition as sr
from gtts import gTTS
import os
import wikipedia

r = sr.Recognizer()

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('start output.mp3')

def recognize_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='en-IN')
        print("Recognized text: " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results: " + str(e))
        return None

def greet():
    speak("Hello! How can I assist you?")

def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia, " + results)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        speak("Did you mean one of the following: " + ", ".join(options))
    except wikipedia.exceptions.PageError:
        speak("Sorry, I could not find any information on that topic.")

def main():
    greet()
    while True:
        text = recognize_speech()
        if text:
            if "wikipedia" in text.lower():
                query = text.lower().replace("wikipedia", "")
                search_wikipedia(query)
            elif "stop" in text.lower():
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I can only search information on Wikipedia.")

if __name__ == "__main__":
    main()
