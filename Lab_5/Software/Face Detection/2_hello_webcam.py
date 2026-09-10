import cv2                       # openCV library version, e.g. 4.10

cap = cv2.VideoCapture(0)        # open and block default camera
while cv2.waitKey(15) != 27:     # 15 ms wait, stop with <ESC>
    ret, frame = cap.read()      # read frame, ignore success flag
    cv2.imshow("Webcam - 'Esc' to quit", frame)  # show frame in window with title
    
cap.release()                    # release camera
cv2.destroyAllWindows()          # close all opencv windows

print(frame.shape)