import cv2
import pytesseract
import pyttsx3
from picamera2 import Picamera2
from PIL import Image
import os
import time
import RPi.GPIO as GPIO

# GPIO setup
BUTTON_2_PIN = 13 
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Set up the camera
camera = Picamera2()
camera_config = camera.create_preview_configuration(main={"size": (640, 480)})
camera.configure(camera_config)
camera.start()

# Initialize the TTS engine
engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 40)  
message = "Position your book well,and press the button again to read"
engine.say(message)
engine.runAndWait()
# female, United States English
for voice in engine.getProperty('voices'):
    if "female" in voice.name.lower() and "english" in voice.languages and "us" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break


pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  

# Set the directory for saved images
save_directory = "/home/john/Desktop/extracts"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Function to extract text and read it aloud
def extract_text_and_speak(image_path):
    # Open the image file
    img = Image.open(image_path)
    
    # Convert image to grayscale (optional)
    img = img.convert('L')
    
    # Extract text using Tesseract
    text = pytesseract.image_to_string(img)
    
    # Check if any text was extracted
    if text.strip():  # If there's text, speak it
        print("Extracted Text:\n", text)
        engine.say(text)
    else:  # If no text is found, print and speak a message
        print("No text found")
        engine.say("No text found")
    
    engine.runAndWait()

# Counter for image filenames
image_counter = 1

# Track last press time for debounce
last_press_time = 0
DEBOUNCE_DELAY = 0.3  # 300ms debounce delay

print("Press the button to capture an image and extract text. Press Ctrl+C to exit.")

try:
    while True:
        # Capture live preview from the camera
        frame = camera.capture_array()
        
        # Display the live feed in an OpenCV window
        cv2.imshow("Camera Preview", frame)
        
        # Check for button press
        if GPIO.input(BUTTON_2_PIN) == GPIO.HIGH:
            current_time = time.time()
            if current_time - last_press_time > DEBOUNCE_DELAY:
                # Update the last press time
                last_press_time = current_time
                
                # Save the current frame to an image file
                print("Button pressed, capturing image...")
                image_path = os.path.join(save_directory, f"captured_image{image_counter}.jpg")
                cv2.imwrite(image_path, frame)
                print(f"Image saved at {image_path}")
                
                # Extract text and speak it
                extract_text_and_speak(image_path)
                
                # Increment the counter for the next capture
                image_counter += 1
        
        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting program...")
            break

except KeyboardInterrupt:
    print("Exit button pressed, stopping program...")
finally:
    print("Cleaning up resources...")
    camera.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()
