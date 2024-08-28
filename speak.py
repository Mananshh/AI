import pyttsx3

def speak(audio):
    print(audio)
    engine = pyttsx3.init('sapi5') #sapi5 is microsofts speech api , helps recoganize the speech input
    voices= engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    
    engine.say(audio)
    engine.runAndWait() #Makes the speech audible
