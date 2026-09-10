""" Get execution time of face Detection with different backend models"""

from deepface import DeepFace
import time
 
backends = [
  'opencv', 
  'ssd', 
  'mtcnn', 
  'retinaface',
]
 
for backend in backends:
        
    #face detection
    start = time.time()
    face_objs = DeepFace.extract_faces(
        img_path = "image.jpg", 
        detector_backend = backend,
        align = False,
    )
    stop = time.time()
    print(f"Face detection with {backend} took {stop-start:.3f} seconds, found {len(face_objs)} face(s)")

face_objs