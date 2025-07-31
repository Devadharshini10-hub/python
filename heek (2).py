
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser  # Import the webbrowser module for opening URLs
import sys  # Needed for graceful shutdown

# Initialize the listener and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Voice selection improvement
voices = engine.getProperty('voices')
voice_index = 3  # Default to the second voice; adjust based on your system
if len(voices) > voice_index:
    engine.setProperty('voice', voices[voice_index].id)
else:
    print(f"Warning: Voice index {voice_index} is out of range. Using default voice.")


def talk(text):
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 0.7)
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice).lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                print(command)
            return command
    except sr.UnknownValueError:
        talk("Sorry, I didn't understand that. Please try again.")
    except sr.RequestError:
        talk("Please check your internet connection.")
    except sr.WaitTimeoutError:
        talk("Listening timed out while waiting for phrase to start. Please speak louder.")


def run_alexa():
    command = take_command()
    if command:
        if 'play' in command:
            song = command.replace('play', '').strip()
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)
        elif 'who the heck is' in command:
            person = command.replace('who the heck is', '').strip()
            try:
                info = wikipedia.summary(person, sentences=1)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk("Sorry, I couldn't find information about that person. Please be more specific.")
        elif 'date' in command:
            talk('Sorry, I have a headache')
        elif 'are you single' in command:
            talk('I am in a relationship with Wi-Fi')
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'open google' in command:
            talk('Opening Google')
            webbrowser.open('https://www.google.com')
        elif 'stop' in command:
            talk('Goodbye!')
            sys.exit()  # Gracefully shutdown
        else:
            talk('Please say the command again.')


while True:
    run_alexa()