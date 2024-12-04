import cv2
import pytesseract
import pyttsx3
from picamera2 import Picamera2
from PIL import Image
import os

# Set up the camera
camera = Picamera2()
camera_config = camera.create_preview_configuration(main={"size": (640, 480)})
camera.configure(camera_config)
camera.start()

# Initialize the TTS engine
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 10)

# Specify the path to Tesseract (you may need to adjust this on Raspberry Pi)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"  # Adjust to your Tesseract path

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
    print("Extracted Text:\n", text)
    
    # Use pyttsx3 to read the extracted text
    engine.say(text)
    engine.runAndWait()

# Counter for image filenames
image_counter = 1

# Preview and capture loop
while True:
    # Capture frame for preview
    frame = camera.capture_array()
    cv2.imshow("Preview - Press Space to Capture", frame)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == 32:  # Spacebar to capture
        # Create a unique filename for each capture
        image_path = os.path.join(save_directory, f"captured_image{image_counter}.jpg")
        cv2.imwrite(image_path, frame)
        
        # Extract text and speak it
        extract_text_and_speak(image_path)
        
        # Increment the counter for the next capture
        image_counter += 1
    elif key == 27:  # Escape to exit
        break

# Cleanup
camera.stop()
cv2.destroyAllWindows()
