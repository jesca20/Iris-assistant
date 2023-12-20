import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import smtplib
import pywhatkit
import random
import requests

MASTER = 'Jessica'
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 160)
activated = False

def say(text):
    engine.say(text)
    engine.runAndWait()

def wake_word():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Waiting for action word.......")
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                wake_word = recognizer.recognize_google(audio).lower()

                if "wake up iris" in wake_word:
                    say("Iris Activated, How may I help you today?")
                    return True

                else:
                    say("Did not recognize the wake-up phrase. Please try again.")
                    
            except sr.UnknownValueError:
                say("Sorry, I couldn't understand the audio. Please try again.")
            except sr.RequestError as e:
                say(f"Speech recognition request failed; {e}")
            except Exception as e:
                say(f"An unexpected error occurred: {e}")
                continue

def greet(command):
    global activated
    greetings = [
        "Hey", "Hello", "Hi", "Hola", "Aloha", "Sup", "Yo", "Ciao", "Wassup",
        "Howdy", "Bonjour", "G'day", "Salute", "Namaste", "whats up",
    ]

    responses = [
        "Hey there! How's it going?", "Hello! Nice to see you!", "Hi! What's up?",
        "Hola! How's your day?", "Aloha! Long time no see!", "Sup! How've you been?",
        "Yo! What's the latest?", "Ciao! Ready for some fun?", "Wassup! Anything exciting happening?",
        "Howdy! What's the scoop?", "Bonjour! How's life treating you?", "G'day! Ready for a good time?",
        "Salut! What's the word?", "Namaste! How's your inner peace today?",
    ]

    recognized_greeting = [word for word in greetings if word.lower() in command.lower()]
    if recognized_greeting:
        random_response = random.choice(responses)
        say(random_response)

def inputcommand():
    recognize = sr.Recognizer()
    with sr.Microphone() as source:
        print('Waiting for the command')
        recognize.adjust_for_ambient_noise(source)

        try:
            audio = recognize.listen(source, timeout=5)
            print('Processing...')
            query = recognize.recognize_google(audio, language='en-us')
            print(f'{query}\n')
            return query.lower()

        except sr.UnknownValueError:
            say("Sorry, I couldn't understand the audio. Please try again.")
        except sr.RequestError as e:
            say(f"Speech recognition request failed; {e}")
        except Exception as e:
            say(f"An unexpected error occurred: {e}")
            return None

def send_email():
    try:
        say('Opening Gmail in browser')
        webbrowser.open("https://mail.google.com")

    except Exception as e:
        say(f"An error occurred: {e}")

def get_joke():
    try:
        joke_url = "https://v2.jokeapi.dev/joke/Any"
        joke_response = requests.get(joke_url)
        joke_data = joke_response.json()

        if joke_data['type'] == 'twopart':
            return f"{joke_data['setup']} {joke_data['delivery']}"
        else:
            return joke_data['joke']

    except requests.RequestException as e:
        say(f"Failed to fetch a joke; {e}")
    except Exception as e:
        say(f"An unexpected error occurred: {e}")

    return "I couldn't fetch a joke at the moment. Sorry!"


def playmusic():
    try:
        say('Sure, playing music on YouTube.')
        pywhatkit.playonyt('lofi beats')
    except pywhatkit.PyWhatKitException as e:
        say(f"Failed to play music; {e}")
    except Exception as e:
        say(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
 if wake_word():
    while True:
            command = inputcommand()
            if command:
                greet(command)
                if 'play music' in command:
                    playmusic()
                    pass
                elif 'send email' in command:
                    say('Opening Gmail in browser')
                    send_email()
                    pass
                elif 'tell me a joke' in command:
                    joke = get_joke()
                    pass
                elif 'checktime' in command:
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    say(f"The current time is {current_time}")
                    pass
                elif 'open browser' in command:
                    say("Opening the browser. What would you like to search for?")
                    webbrowser.open("https://www.google.com")
                    pass
                elif 'search' in command:
                    search_query = command.replace('search', '')
                    say(f"Searching for {search_query}")
                    pywhatkit.search(search_query)
                    pass
                elif 'exit' in command:
                    say("Goodbye, Have a nice day.")
                    break
                else:
                    say("I'm not sure how to handle that request. Can you please clarify?")
