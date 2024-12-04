import pyttsx3
import time
import RPi.GPIO as GPIO
from datetime import datetime

# Initialize pyttsx3 TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', engine.getProperty('rate') - 10)

# GPIO setup for the time button
TIME_BUTTON_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(TIME_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to announce time
def say_time():
    current_time = datetime.now().strftime("%I:%M %p")  # Example: 03:45 PM
    time_message = f"The current time is {current_time}"
    print(time_message)
    engine.say(time_message)
    engine.runAndWait()

# Function to announce date
def say_date():
    current_date = datetime.now().strftime("%A %d %B %Y")  # Example: Saturday 6 April 2024
    date_message = f"Today is {current_date}"
    print(date_message)
    engine.say(date_message)
    engine.runAndWait()

# Track if the button was pressed recently
last_press_time = None
time_threshold = 1  # Minimum interval (seconds) between presses for detecting a second press

try:
    # Initial startup message
    print("Press the button to hear the current time or date.")
    engine.say("Press the button to hear the current time or date.")
    engine.runAndWait()

    while True:
        if GPIO.input(TIME_BUTTON_PIN) == GPIO.LOW:
            # Check if a second press occurred within the threshold
            current_press_time = time.time()
            if last_press_time and (current_press_time - last_press_time) < time_threshold:
                # Announce the date if pressed again within threshold
                say_date()
                last_press_time = None  # Reset after saying the date
            else:
                # Announce the time if it's the first press
                say_time()
                last_press_time = current_press_time
            # Debounce delay
            time.sleep(0.3)

        time.sleep(0.1)  # Polling interval for button press

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    # Shutdown message
    print("Time program exiting.")
    engine.say("Time program exiting.")
    engine.runAndWait()
    GPIO.cleanup()
