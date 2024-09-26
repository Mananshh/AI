import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Get and print the available voices
voices = engine.getProperty('voices')

for index, voice in enumerate(voices):
    print(f"Voice {index}:")
    print(f"ID: {voice.id}")
    print(f"Name: {voice.name}")
    print(f"Gender: {voice.gender}")
    print(f"Languages: {voice.languages}\n")

    # Set the voice and speak a sample text
    engine.setProperty('voice', voice.id)
    engine.say("Hello, I am testing this voice.")
    engine.runAndWait()

engine.stop()
