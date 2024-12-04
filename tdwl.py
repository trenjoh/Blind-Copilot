import pyttsx3
from datetime import datetime
import geocoder

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

def announce_date():
    try:
        # Get the current date
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        message = f"Today's date is {current_date}"
        print(message)
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print(f"Error announcing date: {e}")

def announce_location():
    try:
        # Get the current location using geocoder
        location = geocoder.ip('me')
        if location.ok:
            message = f"Your current location is {location.city}, {location.country}"
        else:
            message = "Location could not be determined."
        print(message)
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print(f"Error announcing location: {e}")

print("Type 'v' and press Enter to announce the date or 'n' and press Enter to announce the location.")

# Wait for user input
while True:
    user_input = input("Press 'v', 'n', or 'q' to quit: ").strip().lower()
    if user_input == 'v':
        announce_date()
    elif user_input == 'n':
        announce_location()
    elif user_input == 'q':
        print("Exiting program.")
        engine.say("exiting")
        engine.stop()
        break
    else:
        print("Invalid input, please press 'v', 'n', or 'q'.")
