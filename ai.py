import pyttsx3 # this helps with speech recognition 
import speech_recognition as sr 
import datetime 
import webbrowser
import data
import csv
import wikipedia
import smtplib
import AppOpener

def wishme(name):
    hour = int(datetime.datetime.now().hour)
    if 0<= hour < 12:
         speak(f"Good Evening {name}")
    elif 12<= hour <= 18:
         speak("Good Afternoon {name}")
    else:
         speak("Good Evening {name}")


def speak(audio):
    print(audio)
    engine = pyttsx3.init('sapi5') #sapi5 is microsofts speech api , helps recoganize the speech input
    voices= engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    
    engine.say(audio)
    engine.runAndWait() #Makes the speech audible
    

def input_voice():
    r = sr.Recognizer()
    with sr.Microphone as source:
        print("Listening....")
        r.pause_threshold = 1 
        audio = r.listen(source)

    try:
            print("Recognizing...")    
            query = r.recognize_google(audio, language='en-in') 
            print(f"User said: {query}\n")
    except Exception as e: 
            speak("Say that again please...")

def sendEmail(recipient, text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    '''
    Import Data,  contacts as csv file or something
    '''
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', recipient, text)
    server.close()


def acc_check():
    try:
        with open("data.csv" , "r", newline= '') as file:
            reader1 = csv.DictReader(file)
            rows1 = [r for r in reader1]
            lastrow1 = rows1[-1]
            name = lastrow1[-1]
    except Exception:
        speak("No user found , Creating Account")
        speak("Please tell me your name")
        #name = input_voice()
        name = input("name ")
        speak(f"Hello, {name} ,please enter your email, you're gonna have to type this one.")
        email = input("Enter Email here")
        data.create_info(name , email)
        speak("Info created , please enter query")

acc_check()


while True:
    try:
       query = input("query")
       #query = input_voice.lower()
    except Exception as e:
         speak(f"Uh oh, {e} found")
         break
    if "create profile" in query:
         with open("data.csv" , "r") as file:
              reader = csv.DictReader(file)
              rows = [r for r in reader]
              lastrow = rows[-1]
              wishme(lastrow["Name"])
              speak("Please tell me your name")
              #name = input_voice()
              name = input("name ")
              speak(f"Hello, {name} ,pls enter your email, you're gonna have to type this one.")
              email = input("Enter Email here")
              data.create_info(name , email)
              speak(f"Hello {name}, profile succesfully created , pls proceed with further queries ")
    elif "open google" in query:
         speak("Opening Google")
         webbrowser.open("google.com")
    elif "wikipedia" in query:
        searchm = query.replace("wikipedia" , "")
        results = wikipedia.summary(query, sentences=3)
        speak("According to Wikipedia")
        speak(results)    
    elif "send email" in query:
        try:
            speak("What should I say?")
            text = input_voice()
            recipient = "sample@gmail.com"    
            sendEmail(recipient, text)
            speak("Email has been sent!")
        except Exception:
            speak("Error sending the email. Please try again")
    elif "open youtube" in query:
        speak("Opening Youtube")
        webbrowser.open("youtube.com")
    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"Sir, the time is {strTime}")
    elif "open discord" in query:
         speak("Opening Discord")
         AppOpener.open("discord")
    elif "open telegram" in query:
         AppOpener.open("telegram")
    elif ("goodbye" or "goodnight" or "quit" or "peace out") in query:
         speak("Turning off, Thankyou for using this A.I.")
         break
    else:
         speak("Unrecoganized command, Please try again")
         