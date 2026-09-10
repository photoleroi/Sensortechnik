import cv2

cap = cv2.VideoCapture(1)
while cv2.waitKey(15) != 27 :
    ret, frame = cap.read()
    cv2.imshow("Webcam", frame[:,:,1])
    print(frame.shape)
cap.release()
cv2.destroyAllWindows()