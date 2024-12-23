#model_3
#model 2
#model_1.tflite
import numpy as np
import cv2
import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2, Preview

try:
    # Load the TFLite model
    interpreter = tflite.Interpreter(model_path="/home/john/Desktop/model_4.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print(f'Input shape: {input_details[0]["shape"]}')  # Print expected input shape

    # Initialize PiCamera2
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))  # Set a larger preview size
    picam2.start()

    while True:#Wrapped the image capture and processing to allow for continuous preview and processing
        # Capture image from PiCamera
        img = picam2.capture_array()

        # Display the live camera feed
        cv2.imshow('Camera Preview', img)

        # Process the image
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB if necessary
        img_rgb = cv2.resize(img_rgb, (input_details[0]['shape'][2], input_details[0]['shape'][1]))  # Resize to match model input
        img_rgb = img_rgb.astype(np.float32)  # Convert to float32
        img_rgb = np.expand_dims(img_rgb, axis=0)  # Add batch dimension

        # Normalize the image if required by the model (between 0 and 1)
        img_rgb /= 255.0

        # Set the input tensor
        interpreter.set_tensor(input_details[0]['index'], img_rgb)

        # Run inference
        interpreter.invoke()

        # Get the output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predicted_class_index = np.argmax(output_data)

        # Mapping class indices to labels
        class_labels = {0: 'banana', 1: 'cups', 2: 'pen', 3: 'phone', 4: 'specs'}
        # Print predicted class label instead of index
        predicted_class_label = class_labels.get(predicted_class_index, "Unknown class")
        print(f'Predicted class: {predicted_class_label}')

        # Save the captured image
        cv2.imwrite('/home/john/Desktop/captured_image5.jpg', img)  # Change the path if needed

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f'Error: {e}')

finally:
    picam2.stop()  # Ensure the camera is stopped
    cv2.destroyAllWindows()  # Close the OpenCV window
