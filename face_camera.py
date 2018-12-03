# coding: utf-8

import face_recognition
import cv2
import numpy as np

from PIL import Image
from utils import draw_bounding_box_on_image


fanhua_image = face_recognition.load_image_file("images/fanhua.jpg")
fanhua_face_encoding = face_recognition.face_encodings(fanhua_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    fanhua_face_encoding
]
known_face_names = [
    u"樊华"
]

def detect_faces(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    resize_scale = 2.0
    frame = cv2.resize(frame, (0, 0), fx=1/resize_scale, fy=1/resize_scale)

    face_locations = face_recognition.face_locations(frame, model='cnn')
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= resize_scale
        right *= resize_scale
        bottom *= resize_scale
        left *= resize_scale

        draw_bounding_box_on_image(image, top, left, bottom, right, font="SimKai", 
                display_str_list=[name], use_normalized_coordinates=False)

    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    return image