from time import sleep
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pyttsx3
import datetime as dt
import speech_recognition as sr
import wikipedia
import webbrowser
from keyboard import press
from keyboard import press_and_release
import winsound
from GetSong import *
import smtplib

# Setting variable from setup.txt here
# TOKEN = 'BQCXlVUBUtzcyOpndk3lG2gMczg4SQ7ImRUFXzrITHyVc_qWNl30RlnSYW0J3vdUj7TjcYPnawgJ8SPzcXTsqXvodCBEDFW_ZP_PShfvwRuehOtIjqSHJr4X7zez9_wukPER5rCpq8lwiPLz9Gsu7g24uz6z-SQiueqDR5w2msTgs4ybpu0R9r5KUw", "token_type": "Bearer", "expires_in": 3600, "refresh_token": "AQB637j2pDU6-KVW91OoMKjzTvr8SuwpDzMwbR_rvUxA19Ie4tCeRjj0dv2aALwfA7sRGGErCJnXFqIBEb6D52sZplRU08d9WXHImE9RbafYc4BqjULfSZrXURRdHder-UA' 
# headers = {
#     "Accept" : "application/json",
#     "Content-Type" : "application/json",
#     "Authorization" : "Bearer {token}".format(token=TOKEN)
# }


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(voice):
    engine.say(voice)
    engine.runAndWait()


try:
    setup = pd.read_csv('E:/setup.txt', sep='=', index_col=0, squeeze=True, header=None)
    client_id = setup['client_id']
    client_secret = setup['client_secret']
    username = setup['username']
    redirect_url = setup['redirect_url']
    scope = setup['scope']
    device_name = setup['device_name']

    # Connecting to spotify
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url,
                                scope=scope, username=username, show_dialog=True)

    spotify = sp.Spotify(auth_manager=auth_manager)
    # selecting device to play spotify on
    devices = spotify.devices()
    for d in devices['devices']:
        d['name'] = d['name'].replace('`', '\'')
        print(d['name'])
        if d['name'] == device_name:
            deviceID = d['id']
            break
except Exception as e:
    print("Net Not Available")
    speak("Please Check your Internet Connection")
    exit()

i = 0


def wishMe():
    hour = int(dt.datetime.now().hour)
    if (hour >= 0) and (hour < 12):
        speak("Good Morning")
    elif (hour >= 12) and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("This is Jarvis. Please tell me something to do")


def takeCommand():
    '''This is the function that take voice commands and converts it into string'''
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        r.pause_threshold = 0.5
        r.energy_threshold = 100
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language="en-in")
        print("User Said: ", query, "\n")
    except Exception as e:
        print(e)
        i = -1
        print("Say that again Please...")
        speak("Say That Again Please")
        return "None"
    return query


def call():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        r.pause_threshold = 0.5
        r.energy_threshold = 100
        print("Listening")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        if query.lower() == "jarvis":
            print("User Said: ", query, "\n")
        else:
            pass
    except Exception as e:
        print("")
        return "None"
    return query


def sendEmail(sender, passowrd, to, msg):
    servers = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        servers.ehlo()
        servers.starttls()
        servers.login(sender, passowrd)
        servers.sendmail(sender, to, msg)
        print("Sent Email")
        speak("Email Sent Successfully")
    except Exception as e:
        print(e)
        speak("Could not send email")
    finally:
        servers.close()


if __name__ == "__main__":
    wishMe()
    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
    while True:
        query = ""
        if i == 0:
            query = takeCommand().lower()
        else:
            if "jarvis" in call().lower():
                winsound.PlaySound("beep.wav", winsound.SND_ALIAS)
                query = takeCommand().lower()
            else:
                pass
        if query == "tell me the time" or query == "tell me time" or query == "time":
            times = dt.datetime.now().strftime("%H:%M:%S")
            print(times)
            speak(times)
        if "wikipedia" in query:
            speak("Searching wikipedia")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                print("According to wikipedia: ", results)
                speak("According to wikipedia ")
                speak(results)
            except Exception as e:
                speak("Sorry nothing matches " + query)
        if "open youtube" in query:
            webbrowser.get('chrome').open("youtube.com")
        elif "youtube" in query:
            if "on youtube" in query:
                query = query.replace(" on", "")
            query = query.replace("youtube", "")
            if query == "":
                webbrowser.get('chrome').open("youtube.com")
            else:
                webbrowser.get('chrome').open("youtube.com/results?search_query=" + query)
        elif "play" in query and "youtube" in query:
            if "on youtube" in query:
                query = query.replace(" on", "")
            query = query.replace("play", "")
            query = query.replace("youtube", "")
            if query == "":
                webbrowser.get('chrome').open("youtube.com")
            else:
                webbrowser.get('chrome').open("youtube.com/results?search_query=" + query)
        elif "open" in query and "youtube" in query:
            if "on youtube" in query:
                query = query.replace(" on", "")
            query = query.replace("open", "")
            query = query.replace("youtube", "")
            if query == "":
                webbrowser.get('chrome').open("youtube.com")
            else:
                webbrowser.get('chrome').open("youtube.com/results?search_query=" + query)
        elif "search" in query and "youtube" in query:
            if "on youtube" in query:
                query = query.replace(" on", "")
            query = query.replace("search", "")
            query = query.replace("youtube", "")
            if query == "":
                webbrowser.get('chrome').open("youtube.com")
            else:
                webbrowser.get('chrome').open("youtube.com/results?search_query=" + query)
        if "open google" in query:
            webbrowser.get('chrome').open("https://")
        elif "google" in query:
            query = query.replace("google", "")
            if query == "":
                webbrowser.get('chrome').open("https://")
            else:
                webbrowser.get('chrome').open("google.com/search?q=" + query)
        if 'on spotify' in query:
            query = query.replace("on spotify", "")
            if 'play' in query:
                query = query.replace("play", "")
            speak("Playing")
            webbrowser.get('chrome').open('open.spotify.com/search/' + query)
            sleep(7)
            press('enter')
            press('space bar')
            # words = query.split()
            # sname = ' '.join(words[1:])
            # try:
            #     if words[0] == "album":
            #         uri = get_album_uri(spotify,sname)
            #         play_album(spotify,deviceID,uri)
            #     elif words[0] == "artist":
            #         uri = get_artist_uri(spotify,sname)
            #         play_artist(spotify,deviceID,uri)
            #     elif words[0] == "play":
            #         uri = get_track_uri(spotify,sname)
            #         play_track(spotify,deviceID,uri)
            #     else:
            #         print("Specify play artist or album")
            #         speak("Specify play artist or album")
            # except Exception as e:
            #     print(e)
            #     speak("Could not get "+sname+" from spotify")
        if "open spotify" in query:
            query = query.replace("open spotify", "")
            speak("opening")
            webbrowser.get('chrome').open('open.spotify.com')
            sleep(7)
            press("space bar")
        if "send email" in query or "send an email" in query or "email" in query:
            sender = "panditved3@gmail.com"
            password = setup["password"]
            speak("Please enter email address of receiver")
            receivers = input("Enter the email address(es) of receiver(s) separated by space:")
            receiver = receivers.split()
            msg = ""
            speak("Do you want to type mail content or tell mail content?")
            question = takeCommand()
            while question == "None":
                question = takeCommand()
            if "tell" in question or "speak" in question:
                speak("What is to be emailed? ")
                msg = takeCommand()
                while msg == "None":
                    msg = takeCommand()
            elif "write" in question or "type" in question:
                msg = input("Enter the message:")
            else:
                speak("Sorry I didn't hear that correctly please type the content")
                msg = input("Enter the mail body:")
            sendEmail(sender, password, receiver, msg)
        if "hello" == query or "hi" ==  query:
            print("Hey There How are you!!")
            speak("Hey There. How are you!!")
            i=-1
        if "i am fine" in query or "how are you" in query:
            print("I am fine. Thank you for being concerned")
            speak("I am fine. Thank you for being concerned")
        if query == "exit" or query == "bye" or query == "good bye" or query == "goodbye" or query == "please leave":
            speak("Good Bye Sir")
            exit()
        i += 1
