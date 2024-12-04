import pyttsx3
from datetime import datetime
# Initialize the pyttsx3 engine
engine = pyttsx3.init()
# Get the current time in 12-hour format with AM/PM
current_time = datetime.now().strftime("%I:%M %p")
# Define the message to speak
message = f"The current time is {current_time}"
print(message)
# Use pyttsx3 to speak the message
engine.say(message)
engine.runAndWait()

engine.stop()

