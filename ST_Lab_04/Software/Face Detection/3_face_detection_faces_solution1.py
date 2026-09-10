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
    # convert face_obj["face"] to uint8 and from RGB to BGR and show the image using opencv
    face_uint8 = (face_obj["face"] * 255).astype(np.uint8) # convert to uint8
    face_bgr = cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR) # convert to BGR
    
    cv2.imshow(f"Face #{i}", face_bgr)
    # move the window to a new position
    cv2.moveWindow(f"Face #{i}", 10 + i % GRID_SIZE * TILE_WIDTH, 10 + i // GRID_SIZE * TILE_HEIGHT)
    print(f"Face #{i} shape: {face_obj['face'].shape}")

cv2.waitKey(0)              # show all images and wait for a key press
cv2.destroyAllWindows()     # close all windows