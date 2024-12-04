import cv2
from time import sleep
from picamera2 import Picamera2

camera = Picamera2()
camera_config = camera.create_preview_configuration(main={"size": (640, 480)})
camera.configure(camera_config)
camera.start()


for _ in range(60):  
    frame = camera.capture_array()
    cv2.imshow("Preview", frame)
    if cv2.waitKey(100) == ord('q'): 
        break


camera.capture_file('2jn.jpg')

# Clean up
camera.stop()
cv2.destroyAllWindows()
