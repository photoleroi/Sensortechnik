""" Face Detection with different backend models"""


from deepface import DeepFace
import cv2
import numpy as np
 
IMG_PATH = "image.jpg"
BACKEND = 'mtcnn'
GRID_SIZE = 10
TILE_WIDTH = 150
TILE_HEIGHT = 100
 
face_objs = DeepFace.extract_faces(
    img_path = IMG_PATH, 
    detector_backend = BACKEND,
    align = False,
)
print(f"Face detection with {BACKEND} found {len(face_objs)} faces")
    
# show the image using opencv and detector backend
for i, face_obj in enumerate(face_objs):
    # TODO: finden und korrigiere den Fehler
    face = face_obj["face"]
    
    cv2.imshow(f"Face #{i}", face)
    # move the window to a new position
    cv2.moveWindow(f"Face #{i}", 10 + i % GRID_SIZE * TILE_WIDTH, 10 + i // GRID_SIZE * TILE_HEIGHT)
    print(f"Face #{i} shape: {face_obj['face'].shape}")

cv2.waitKey(0)              # show all images and wait for a key press
cv2.destroyAllWindows()     # close all windows