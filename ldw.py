import pyttsx3
from datetime import datetime
import geocoder
import time
# Initialize the pyttsx3 engine
engine = pyttsx3.init()


message = "Get your location and date query"
print(message)
engine.say(message)
engine.runAndWait()  
time.sleep(0.5)
# Announce the current date
current_date = datetime.now().strftime("%A, %B %d, %Y")
message = f"Today's date is {current_date}"
print(message)
engine.say(message)
engine.runAndWait()  
time.sleep(0.5)
# Get the current location using geocoder
location = geocoder.ip('me')
if location.ok:
    message = f"Your current location is {location.city}, {location.country}"
else:
    message = "Location could not be determined."

# Announce the locationS
print(message)
engine.say(message)
engine.runAndWait()  
time.sleep(1)


engine.stop()
