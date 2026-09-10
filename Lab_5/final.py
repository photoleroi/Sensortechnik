from djitellopy import Tello
import cv2
import socket
import threading
import socket
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

face = 0


#def flight_thread():
#    pass


def main():
    global face
    tello = Tello()
    tello.connect()
    tello.streamon()
    tello.takeoff()
    tello.send_rc_control(0, 0, 0, 0)
    #time.sleep(2)
    tello.move_up(150)

    while face < 2:
        img = tello.get_frame_read().frame

        img = cv2.resize(img, (600, 600))

        cv2.imshow("Image", img)
        tello.send_rc_control(0, 0, 0, 30)

        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minSize=(30, 30))

        face = len(faces)
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imwrite('face' + str(face) + '.jpg', img)  # save frame as JPEG file
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(face)
    tello.land()
    tello.streamoff()


if __name__ == "__main__":
    main()
