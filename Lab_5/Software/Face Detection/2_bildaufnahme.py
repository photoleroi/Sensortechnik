""" Capture images from webcam and save them to disk. 
    Press 'Space' to save picture as image.jpg
    Press 'ESC' to quit the program 
    
    @author: Joerg
    @creation: 2024-09-20"""

import cv2

CAM_ID = 0  # 0 for default camera

cap = cv2.VideoCapture(CAM_ID)

while cv2.waitKey(1) != 27:
    ret, frame = cap.read()
    cv2.imshow("Press 'Space' to save picture and 'Esc' to quit", frame)
    if cv2.waitKey(1) == ord(' '):
        cv2.imwrite("image.jpg", frame)
        print("Image saved.")

cap.release()
cv2.destroyAllWindows()