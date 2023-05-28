import speech_recognition as sr

def voice_input():
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
    except sr.RequestError as e:
        print("Error occurred: {0}".format(e))
