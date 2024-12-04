import RPi.GPIO as GPIO
import time
import os
import pyttsx3
import subprocess
import cv2
import pytesseract
from picamera2 import Picamera2
from PIL import Image

# Initialize pyttsx3 TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', engine.getProperty('rate') - 10)

# GPIO setup
BUTTON_1_PIN = 6  # Button for Object Detection
BUTTON_2_PIN = 13  # Button for Text Extraction
BUTTON_3_PIN = 19  # Button for Telling Time
BUTTON_4_PIN = 26  # Button for Safe Shutdown
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set up Tesseract path if required
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Global variable to hold the running process
current_process = None

# Function to run external programs
def run_program(script_path, message):
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process.wait()
    print(message)
    engine.say(message)
    engine.runAndWait()
    current_process = subprocess.Popen(['python3', script_path])

# Function to extract text and speak it
def extract_text_and_speak(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # Optional: Convert image to grayscale
        text = pytesseract.image_to_string(img)
        if text.strip():  # Speak the extracted text if any
            print("Extracted Text:\n", text)
            engine.say(text)
        else:  # Handle cases where no text is found
            print("No text found")
            engine.say("No text found")
        engine.runAndWait()
    except Exception as e:
        print(f"Error during text extraction: {e}")
        engine.say("An error occurred during text extraction.")
        engine.runAndWait()

try:
    print("Device powered on.")
    engine.say("Device powered on. Please press a button to select a program.")
    engine.runAndWait()

    save_directory = "/home/john/Desktop/extracts"
    os.makedirs(save_directory, exist_ok=True)

    image_counter = 1

    while True:
        if GPIO.input(BUTTON_1_PIN) == GPIO.HIGH:
            run_program("/home/john/Desktop/model_3_v1_with_speech.py", "Starting Object Detection program.")
            time.sleep(0.3)  # Debounce delay

        elif GPIO.input(BUTTON_2_PIN) == GPIO.HIGH:
            print("Position your book well, and press again to read.")
            engine.say("Position your book well, and press again to read.")
            engine.runAndWait()

            # Initialize and start the camera
            camera = Picamera2()
            camera_config = camera.create_preview_configuration(main={"size": (640, 480)})
            camera.configure(camera_config)
            camera.start()

            text_mode = True  # Flag for text decoding mode
            last_press_time = time.time()

            while text_mode:
                frame = camera.capture_array()
                cv2.imshow("Camera Preview", frame)

                if GPIO.input(BUTTON_2_PIN) == GPIO.HIGH:
                    current_time = time.time()
                    if current_time - last_press_time > 0.3:
                        last_press_time = current_time
                        print("Button pressed, capturing image...")
                        image_path = os.path.join(save_directory, f"captured_image_{image_counter}.jpg")
                        cv2.imwrite(image_path, frame)
                        print(f"Image saved at {image_path}")

                        extract_text_and_speak(image_path)
                        image_counter += 1

                elif GPIO.input(BUTTON_1_PIN) == GPIO.HIGH or GPIO.input(BUTTON_3_PIN) == GPIO.HIGH or GPIO.input(BUTTON_4_PIN) == GPIO.HIGH:
                    print("Exiting text decoding mode...")
                    text_mode = False

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting text decoding mode...")
                    text_mode = False

            # Stop the camera and close OpenCV window
            camera.stop()
            cv2.destroyAllWindows()
            time.sleep(0.3)

        elif GPIO.input(BUTTON_3_PIN) == GPIO.HIGH:
            run_program("/home/john/Desktop/time_test.py", "Telling the current time.")
            time.sleep(0.3)

        elif GPIO.input(BUTTON_4_PIN) == GPIO.HIGH:
            print("Button four pressed. Safe shutdown initiated.")
            engine.say("Safe shutdown initiated.")
            engine.runAndWait()
            if current_process and current_process.poll() is None:
                current_process.terminate()
                current_process.wait()
            break

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted.")
    engine.say("Program interrupted. Exiting.")
    engine.runAndWait()

finally:
    print("Device powered off.")
    engine.say("Device powered off.")
    engine.runAndWait()
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process.wait()
    GPIO.cleanup()
