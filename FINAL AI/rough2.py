#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
from groq import Groq
import os

import os
import sys
import threading
import time
import requests
from playsound import playsound

# Custom function to generate audio from the API
def generate_audio(message: str, voice: str = "en-US-Standard-B"):
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except:
        return None

# Function to print text with animation effect
def cooler_print(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the sleep duration for the animation speed
    print()

# Function to play generated speech and delete the audio file
def Co_speak(message: str, voice: str = "en-US-Standard-B", folder: str = "", extension: str = ".mp3"):
    try:
        result_content = generate_audio(message, voice)
        file_path = os.path.join(folder, f"{voice}{extension}")
        with open(file_path, "wb") as file:
            file.write(result_content)
        playsound(file_path)
        os.remove(file_path)
    except Exception as e:
        print(e)

# Function to speak and print text simultaneously
def speak(text):
    # Create threads for both speaking and printing
    t1 = threading.Thread(target=Co_speak, args=(text,))
    t2 = threading.Thread(target=cooler_print, args=(text,))
    
    # Start both threads
    t1.start()
    t2.start()
    
  
    t1.join()
    t2.join()





def custom_print(*objects, sep=' ', end='\n'):
    output = sep.join(map(str, objects))
    # Append the end character(s) to the output
    output += end
    # Return the final output string
    return output


os.environ["GROQ_API_KEY"] = "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"
def custom_str(text, end=""):
    result = str(text) + end
    return result

def loadresponse(query):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    accumulated_text = ""

    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        accumulated_text += content

        if len(accumulated_text) > 1000000 or any(punct in accumulated_text for punct in ['.', '!', '?']):
            speak(accumulated_text)  
            accumulated_text = ""  

    # Process any remaining accumulated text
    if accumulated_text:
        speak(accumulated_text)
q ="tell me 25 random words"

loadresponse(q)