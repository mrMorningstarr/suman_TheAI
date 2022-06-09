import random

import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import smtplib
from secret import senderemail, epwd, email_list , user_name
from email.message import EmailMessage
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import pywhatkit
import requests
from newsapi import NewsApiClient
import clipboard
import os
import subprocess
import pyjokes
import psutil
from nltk.tokenize import word_tokenize



engine = pyttsx3.init()
engine.setProperty('rate', 180)

engine.say("Hello ")
engine.runAndWait()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def getvoices(voice):
    voices = engine.getProperty('voices')

    if voice == 1:
        engine.setProperty('voice', voices[38].id)

    if voice == 2:
        engine.setProperty('voice', voices[29].id)




def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak('time is ')
    speak(Time)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("date is")
    speak(date)
    speak(month)
    speak(year)


def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("good morning sir")
    elif hour >= 12 and hour < 18:
        speak("good afternoon sir")
    elif hour >= 18 and hour < 24:
        speak("good evening sir")
    else:
        speak("good night sir")


def takeCommandCMD():
    query = input("please tell me how can help you?")
    return query


def takeCommandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for background noise. One second")
        r.adjust_for_ambient_noise(source)
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(query)
    except Exception as e:
        print(e)
        speak("say that again sir")
        return "None"
    return query


def sendEmail(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderemail, epwd)
    email = EmailMessage()
    email['From'] = senderemail
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()


def sendwhatsappmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(10)
    pyautogui.press('enter')

def serachgoogle():
    speak('what should I search for?')

    search = takeCommandMIC()
    wb.open('https://www.google.com/search?q='+search)


def news():
    newsapi = NewsApiClient(api_key='42b62fd20fef4b51b843604201a517fd')
    data = newsapi.get_top_headlines(q='bitcoin',
                                     language='en',
                                     page_size=5)
    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print(f'{x}{y["description"]}')
        speak(f'{x}{y["description"]}')

    speak("that's it for now i'll update you in while")

def text2speech():
    text = clipboard.paste()
    print(text)
    speak(text)


def screenshot():
    nam_img = (datetime.datetime.now())
    #nam_img = '\\fallen1\\Downloads'
    img = pyautogui.screenshot(nam_img)
    img.show()

def flip():
    speak("okay sir, flipping a coin")
    coin = ['head', 'tail']
    toss =[]
    toss.extend(coin)
    random.shuffle(toss)
    toss = ("".join(toss[0]))
    speak("i flipped a coin  and you got a "+toss)


def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at" + usage)
    battery = psutil.sensors_battery()
    speak("Battery is at" + battery)
    speak(battery.percent)





if __name__ == '__main__':
    getvoices(2)
    greeting()
    wakeword = "suman"



    while True:
        query = takeCommandMIC().lower()
        query= word_tokenize(query)
        print(query)
        if wakeword in query:



            if 'time' in query:
                time()

            elif 'date' in query:
                date()

            elif 'email' in query:

                try:
                    speak("To whome you want to send")
                    name = takeCommandMIC().lower()
                    receiver = email_list[name]
                    speak("what is the subject of mail")
                    subject = takeCommandMIC()
                    speak('what should i say?')
                    content = takeCommandMIC()
                    sendEmail(receiver, subject, content)
                    speak("email has been sent")
                except Exception as e:
                    print(e)
                    speak("unable to send")




            elif 'offline' in query:
                speak("this is Suman signing off from duty")
                quit()


            elif 'whatsapp' in query:
                try:
                    speak("To whome you want to WhatsApp ")
                    name = takeCommandMIC().lower()
                    phone_no = user_name[name]
                    speak("what is the message?")
                    message = takeCommandMIC().lower()
                    sendwhatsappmsg(phone_no, message)

                    speak("message has been sent")
                except Exception as e:
                    print(e)
                    speak("unable to send")


            elif 'wikipedia' in query:
                speak('searching on wikipedia...')
                query =query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences = 2)
                print(result)
                speak(result)


            elif 'google' in query:
                serachgoogle()



            elif 'youtube' in query:
                speak('what you wanna see on youtube?')
                topic = takeCommandMIC()
                pywhatkit.playonyt(topic)



            elif 'weather' in query:
                url = 'http://api.openweathermap.org/data/2.5/weather?q=indore&units=imperial&appid=c02ad8532b20192c4ae557854406a9ba'
                res = requests.get(url)
                data = res.json()

                weather = data['weather'] [0] ['main']
                temp = data['main']['temp']
                desp = data['weather'][0] ['description']
                temp = round((temp - 32)* 5/9)
                print(weather)
                print(temp)
                print(desp)
                speak('Temperature : {} deegrees celcius'.format(temp))
                speak('weather is {}'.format(desp))

            elif 'news' in query:
                news()


            elif 'read' in query:
                text2speech()



            elif 'covid' in query:
                covid()

            elif 'open' in query:
                speak("what ypu want to open?")
                #codepath = '/usr/share/applications/spyder3.desktop'
                app = takeCommandMIC().lower()
                subprocess.call(app)


            #elif 'documents' in query:
             #   os.popen("cd /home/fallen1/path ; subl")



            elif 'joke' in query:
                speak(pyjokes.get_joke())


            elif 'screenshot' in query:
                screenshot()


            elif 'remember' in query:
                speak("what should i remember?")
                data = takeCommandMIC()
                speak("you said to me "+data)
                remember = open('data.txt','w')
                remember.write(data)
                remember.close()


            elif 'flip' in query:
                flip()


            elif 'cpu' in query:
                cpu()




