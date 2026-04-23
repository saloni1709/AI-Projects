# pip install pyttsx3

import pyttsx3
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define a function to speak text
def speak(text):
    print("AI Bot:", text)
    engine.say(text)
    engine.runAndWait()

# greet
print("Oliver: Hello! I am Python AI assistant. Type 'exit' to end.\n")

# Start chatting loop
while True:
    user_input = input("You: ").lower()

    if user_input == "exit":
        speak("Goodbye!")
        break

    elif "hello" in user_input or "hi" in user_input:
        speak("Hello! I am Oliver. How may I assist you today?")

    elif "how are you" in user_input:
        speak("I am just code, but I feel awesome helping you.")

    elif "time" in user_input:
        current_time = datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")

    elif "calculate" in user_input:
        try:
            result = eval(user_input.replace("calculate", "").strip())
            speak(f"The result is {result}")
        except:
            speak("Sorry, I couldn't understand the calculation.")

    else:
        speak("Sorry, I did not understand that.")