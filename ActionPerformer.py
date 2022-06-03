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
import winsound
from GetSong import *
import smtplib
from prettytable import PrettyTable

class ActionPerform:
    __engine = pyttsx3.init('sapi5')
    voices = __engine.getProperty('voices')
    __engine.setProperty('voice', voices[1].id)
    i = 0
    setup = {}
    __table = PrettyTable(["Srno.", "Searched Query","Time","Date"])
    def speak(self, voice):
        self.__engine.say(voice)
        self.__engine.runAndWait()


    def __init__(self):
        try:
            self.setup = pd.read_csv('E:/setup.txt', sep='=', index_col=0, squeeze=True, header=None)
            client_id = self.setup['client_id']
            client_secret = self.setup['client_secret']
            username = self.setup['username']
            redirect_url = self.setup['redirect_url']
            scope = self.setup['scope']
            device_name = self.setup['device_name']

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
            print("Net Not Available:",e)
            self.speak("Please Check your Internet Connection")
            exit()


    def call(self):
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

    def sendEmail(self, sender, password, to, msg):
        servers = smtplib.SMTP('smtp.gmail.com', 587)
        try:
            servers.ehlo()
            servers.starttls()
            servers.login(sender, password)
            servers.sendmail(sender, to, msg)
            print("Sent Email")
            self.speak("Email Sent Successfully")
        except Exception as e:
            print(e)
            self.speak("Could not send email")
        finally:
            servers.close()
    def takeCommand(self):
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
            self.i = -1
            print("Say that again Please...")
            self.speak("Say That Again Please")
            return "None"
        return query

    def perform(self):
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(
            "C://Program Files//Google//Chrome//Application//chrome.exe"))
        while True:
            query = ""
            if self.i == 0:
                query = self.takeCommand().lower()
            else:
                if "jarvis" in self.call().lower():
                    winsound.PlaySound("beep.wav", winsound.SND_ALIAS)
                    query = self.takeCommand().lower()
                else:
                    continue
            if query == "tell me the time" or query == "tell me time" or query == "time":
                times = dt.datetime.now().strftime("%H:%M:%S")
                print(times)
                self.speak(times)
            if "wikipedia" in query:
                self.speak("Searching wikipedia")
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    print("According to wikipedia: ", results)
                    self.speak("According to wikipedia ")
                    self.speak(results)
                except Exception as e:
                    self.speak("Sorry nothing matches " + query)
            if "open youtube" in query:
                webbrowser.get('chrome').open("youtube.com")
            elif "play" in query and "youtube" in query:
                if "on youtube" in query:
                    query = query.replace(" on", "")
                query = query.replace("play", "")
                query = query.replace("youtube", "")
                if query == "":
                    webbrowser.get('chrome').open("youtube.com")
                else:
                    webbrowser.get('chrome').open(
                        "youtube.com/results?search_query=" + query)
            elif "open" in query and "youtube" in query:
                if "on youtube" in query:
                    query = query.replace(" on ", "")
                query = query.replace("open", "")
                query = query.replace("youtube", "")
                if query == "":
                    webbrowser.get('chrome').open("youtube.com")
                else:
                    webbrowser.get('chrome').open(
                        "youtube.com/results?search_query=" + query)             
            elif "youtube" in query:
                if "on youtube" in query:
                    query = query.replace(" on ", "")
                query = query.replace("youtube", "")
                if query == "":
                    webbrowser.get('chrome').open("youtube.com")
                else:
                    webbrowser.get('chrome').open(
                        "youtube.com/results?search_query=" + query)
            elif "search" in query and "youtube" in query:
                if "on youtube" in query:
                    query = query.replace(" on", "")
                query = query.replace("search", "")
                query = query.replace("youtube", "")
                if query == "":
                    webbrowser.get('chrome').open("youtube.com")
                else:
                    webbrowser.get('chrome').open(
                        "youtube.com/results?search_query=" + query)
            elif "open google" in query:
                webbrowser.get('chrome').open("https://")
            elif "google" in query:
                query = query.replace("google", "")
                if query == "":
                    webbrowser.get('chrome').open("https://")
                else:
                    webbrowser.get('chrome').open("google.com/search?q=" + query)
            elif 'on spotify' in query:
                query = query.replace("on spotify", "")
                if 'play' in query:
                    query = query.replace("play", "")
                self.speak("Playing")
                webbrowser.get('chrome').open('open.spotify.com/search/' + query)
                sleep(10)
                press("enter")
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
            elif "open spotify" in query:
                query = query.replace("open spotify", "")
                self.speak("opening")
                webbrowser.get('chrome').open('open.spotify.com')
                sleep(10)
                press('enter')
                press("space bar")
            elif "send email" in query or "send an email" in query or "email" in query:
                sender = "panditved3@gmail.com"
                password = self.setup["password"]
                self.speak("Please enter email address of receiver")
                receivers = input(
                    "Enter the email address(es) of receiver(s) separated by space:")
                receiver = receivers.split()
                msg = ""
                self.speak("Do you want to type mail content or tell mail content?")
                question = self.takeCommand()
                while question == "None":
                    question = self.takeCommand()
                if "tell" in question or "speak" in question:
                    self.speak("What is to be emailed? ")
                    msg = self.takeCommand()
                    while msg == "None":
                        msg = self.takeCommand()
                elif "write" in question or "type" in question:
                    msg = input("Enter the message:")
                else:
                    self.speak("Sorry I didn't hear that correctly please type the content")
                    msg = input("Enter the mail body:")
                self.sendEmail(sender, password, receiver, msg)
            elif "hello" == query or "hi" == query:
                print("Hey There How are you!!")
                self.speak("Hey There. How are you!!")
                self.i = -1
            elif "i am fine" in query or "how are you" in query:
                print("I am fine. Thank you for being concerned")
                self.speak("I am fine. Thank you for being concerned")
            elif query == "exit" or query == "bye" or query == "good bye" or query == "goodbye" or query == "please leave":
                self.speak("Good Bye Sir")
                exit()
            elif "search history" in query:
                file = open("history.txt","r")
                k=1
                if "today" in query or "todays" in query or "today's" in query:
                    for x in file:
                        column = x.split("|")
                        if str(column[2]) == str(dt.datetime.now().strftime("%d-%B-%Y")+"\n"):
                            print("Hello")
                            column.insert(0,k)
                            self.__table.add_row(column)
                            k+=1
                else:   
                    for x in file:
                        column = x.split("|")
                        column.insert(0,k)
                        self.__table.add_row(column)
                        k+=1
                print(self.__table)
                self.__table.clear_rows()
            else:
                webbrowser.get('chrome').open("google.com/search?q="+query)
            self.i += 1
            if "search history" not in query:
                with open("history.txt","a") as file:
                    file.write(query + "|" + dt.datetime.now().strftime("%H:%M:%S") + "|" + dt.datetime.now().strftime('%d-%B-%Y') +"\n")