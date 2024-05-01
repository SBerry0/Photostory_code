import glob
from os.path import isfile
from pickle import dumps

import cv2
import face_recognition

import constants

FACES_PATH = "results/allFaces"


def encode():
    images = list(filter(isfile, glob.glob(FACES_PATH + "/*")))
    data = []
    print("Encoding...")
    num_images = len(images)
    counter = 1
    for img in images:
        # Embeddings
        image = cv2.imread(img)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="cnn")
        encodings = face_recognition.face_encodings(rgb, boxes)
        d = [{"imagePath": img, "encoding": enc} for enc in encodings]
        data.extend(d)
        print(f"{counter}/{num_images}")
        counter += 1

    # Store data to drive
    print("Saving encodings...")
    f = open(constants.PICKLE_FILENAME, "wb")
    f.write(dumps(data))
    f.close()
    print("Encodings saved")

