# created by Or Nasri

import datetime
import sys
import requests
import smtplib
from selenium import webdriver
import stdiomask
import pyttsx3


# class Shiri, fields: time, pyttsx3 engine, commands
class Shiri:
    # constructor
    def __init__(self):
        self.userName = ""
        self.machine = 'Shiri'
        self.time = datetime.datetime.now().strftime("%H:%M:%S")
        self.driver = 0
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
        self.engine.setProperty('rate', 160)
        self.commands = {"exit": self.exit, "youtube": self.youtube, "search google": self.google,
                         "weather": self.weather, "send mail": self.mail}

    # say hello to user
    def hello(self):
        self.talk("My name is Shiri, Whats your name?")
        self.userName = input()
        self.sayHello(self.userName)

    # main loop of Shiri, waiting fo user command
    def menu(self):
        self.talk("How can I help you?")
        choice = input()
        if choice.lower() not in self.commands.keys():
            self.talk("Command doesn't exist")
            return
        self.commands[choice.lower()]()

    # make Sshiri talk
    def talk(self, string):
        print(string)
        self.engine.say(string)
        self.engine.runAndWait()

    # say hello according to the current time
    def sayHello(self, name):
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            self.talk('Good Morning ' + name)
        elif 12 <= hour < 16:
            self.talk('Good Noon ' + name)
        elif 16 <= hour < 18:
            self.talk('Good Afternoon ' + name)
        elif 18 <= hour < 20:
            self.talk('Good Evening ' + name)
        else:
            self.talk('Good Night ' + name)

    # close program
    def exit(self):
        self.talk("BYE BYE " + self.userName)
        sys.exit()

    # send mail using SMTP server
    def mail(self):
        user = input("Enter gmail: ")
        password = stdiomask.getpass("Enter password: ", '*')
        sent_from = user
        mail_to = input("To: ")
        to = [mail_to]
        subject = input("Subject: ")
        body = input("Body: ")
        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(user, password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            self.talk('Email sent!')
        except Exception:
            self.talk('Something went wrong...')

    # getting weather info from open weather API
    def weather(self):
        text = input("Choose city: ")
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        api_key = "91ed0f9b9c41429b65676e405fee4dc1"
        final_url = base_url + "q=" + text + "&appid=" + api_key
        response = requests.get(final_url)
        dictionary = response.json()
        temp = str(round(dictionary['main']['temp'] - 273.15))
        self.talk(dictionary['weather'][0]['main'] + ", " + temp + "°")

    # playing youtube videos using webdriver
    def youtube(self):
        text = input("Choose video: ")
        if self.driver == 0:
            for i in range(92, 95, 1):
                try:
                    driver = webdriver.Chrome("chromedriver_" + str(i) + ".exe")
                    driver.get("https://youtube.com")
                    search_box = driver.find_element_by_name('search_query')
                    search_box.send_keys(text)
                    search_box.submit()
                    video = driver.find_element_by_id('video-title')
                    video.click()
                    self.driver = i
                    break
                except Exception:
                    continue
        else:
            driver = webdriver.Chrome("chromedriver_" + str(self.driver) + ".exe")
            driver.get("https://youtube.com")
            search_box = driver.find_element_by_name('search_query')
            search_box.send_keys(text)
            search_box.submit()
            video = driver.find_element_by_id('video-title')
            video.click()

    # google search
    def google(self):
        text = input("what to search in google for you: ")
        if self.driver == 0:
            for i in range(92, 95, 1):
                try:
                    driver = webdriver.Chrome("chromedriver_" + str(i) + ".exe")
                    driver.get("https://google.com")
                    search_box = driver.find_element_by_name('q')
                    search_box.send_keys(text)
                    search_box.submit()
                    self.driver = i
                    break
                except Exception:
                    continue
        else:
            driver = webdriver.Chrome("chromedriver_" + str(self.driver) + ".exe")
            driver.get("https://google.com")
            search_box = driver.find_element_by_name('q')
            search_box.send_keys(text)
            search_box.submit()
