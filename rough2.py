# from webscout import PhindSearch as brain
# #Phind search will give more tech, coding realted doubts for you to answer, Llama gives answers to more practical questions
# from rich import print
# from webscout.AIutel import RawDog
# from mainAI import speak
# from mainAI import cooler_print

# rawdog = RawDog()
# intro_prompt = rawdog.intro_prompt

# ai = brain(
#     is_conversation=True,
#     max_tokens=800,
#     timeout=30,
#     intro=intro_prompt,
#     filepath=r"C:\Users\Storm\After Hours(Python)\conversations.txt",
#     update_file=True,
#     proxies={},
#     history_offset=10250,
#     act=None,
# )

# def testingAI(text):
#     response = ai.chat(text)
#     rawdog_feedback = rawdog.main(response)
#     if rawdog_feedback:
#         ai.chat(rawdog_feedback)
#     speak(response)
#     return response


from mainAI import speak
from mainAI import cooler_print
from webscout import LLAMA3 as brain
from rich import print
import os

# Define file paths
history_file = r"C:\Users\Storm\After Hours(Python)\conversations.txt"

def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return file.read()
    return ""

def save_history(history):
    with open(history_file, 'w') as file:
        file.write(history)

# Load existing history
conversation_history = load_history()

# Initialize the AI
ai = brain(
    is_conversation=True,  # AI will remember conversations
    max_tokens=800,
    timeout=30,
    intro=None,
    filepath=None,  # Memory file not used as we handle it manually
    update_file=False,  # No need to update the memory file
    proxies={},
    history_offset=10250,  # Use a high context window model
    act=None,
    model="llama3-70b",
    system="You are a Helpful AI"
)

def testingAI(text):
    conversation_history = load_history()
    # Append the prompt to the conversation history
    conversation_history += f"\nUser: {text}"
    
    # Generate the full prompt including the conversation history
    full_prompt = conversation_history + "\nAI:"
    
    # Get the AI's response
    response_chunks = []
    for chunk in ai.chat(full_prompt):
        response_chunks.append(chunk)
        print(chunk, end="", flush=True) 

    
    # Combine the response chunks into a single response
    response_text = "".join(response_chunks)
    speak(response_text)
    conversation_history += f"\nAI: {response_text}"
    
    if "remember this" in text.lower():
        # Save the updated conversation history
        save_history(conversation_history)
    return response_text

testingAI("How can I modify you to update recent events and do tasks?")