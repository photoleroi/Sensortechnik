""" Face Detection with different backend models
    generating image with bounding box around detected faces"""

# fun fact: extract_faces with ssd backend returns only one face object but there are some hints that it can detect multiple faces
# see: https://stackoverflow.com/questions/69236652/how-to-use-deepface-detectface-to-actually-detect-a-several-faces-in-an-image


from deepface import DeepFace
import cv2
import numpy as np

img_file = "image_group.jpg"
 
backends = [
  'opencv', 
  'ssd', 
  'mtcnn', 
  'retinaface',
]
 
for backend in backends:
    
    img = cv2.imread(img_file)
        
    #face detection
    face_objs = DeepFace.extract_faces(
        img_path = img_file, 
        detector_backend = backend,
        align = False,
    )
    
    # show the image using opencv and detector backend
    for face_obj in face_objs:
        facial_area = face_obj["facial_area"]
        x, y, w, h = facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]
        img_bb = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    title = f"Face Detection with {backend} {len(face_objs)} faces"     
    cv2.imshow(title, img_bb)
    cv2.waitKey(1)          # show image after completion of each backend

cv2.waitKey(0)              # show all images and wait for a key press
cv2.destroyAllWindows()     # close all windows