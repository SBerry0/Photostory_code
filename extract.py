# Extract faces with deepface mtcnn detector (facenet512)
# and store encodings of each face

import glob
import math
import os

import cv2
import numpy as np
from mtcnn import MTCNN
from PIL import Image
from scipy.spatial.distance import euclidean

import encode


def extract_faces(dir):
    images = list(filter(os.path.isfile, glob.glob(dir + "/*")))
    counter = 0
    # TESTING:
    # if __name__ == "__main__":
    #     if not os.path.isdir("results/allImages"):
    #         os.mkdir("results/allImages")
    #     else:
    #         for dir in os.listdir("results/allImages"):
    #             for f in os.listdir("results/allImages/" + dir):
    #                 os.remove("results/allImages/" + dir + "/" + f)
    #             os.rmdir("results/allImages/" + dir)
    #     if not os.path.isdir("results/allFaces"):
    #         os.mkdir("results/allFaces")
    #     else:
    #         for f in os.listdir("results/allFaces"):
    #             os.remove("results/allFaces/" + f)
   
    # For every jpg image, lift the faces
    for image in images:
        print("Image: " + str(counter) + "\nName: " + str(image))
        # Face detection
        img = cv2.cvtColor(cv2.imread(image), cv2.COLOR_BGR2RGB)
        detector = MTCNN(min_face_size=85)
        detections = detector.detect_faces(img)
        
        path = f"results/allImages/image{str(counter)}"
        os.mkdir(path)

        for detection in detections:
            confidence = detection["confidence"]
            if confidence > 0.90:
                # Bounding box and face extraction
                x, y, w, h = detection["box"]
                detected_face = img[int(y):int(y+h), int(x):int(x+w)]

                # Alignment
                keypoints = detection["keypoints"]
                left = keypoints["left_eye"]
                right = keypoints["right_eye"]
                aligned_face = alignment_procedure(detected_face, left, right)

                save = Image.fromarray(aligned_face)
                save.save(f"{path}/{w}{h}_faces.jpg")
                save.save("results/allFaces/" + str(w) + str(h) + '_faces.jpg')
        counter += 1
    

def alignment_procedure(img, left_eye, right_eye):
    left_eye_x, left_eye_y = left_eye
    right_eye_x, right_eye_y = right_eye
    if left_eye_y > right_eye_y:
        point_3rd = (right_eye_x, left_eye_y)
        direction = -1
    else:
        point_3rd = (left_eye_x, right_eye_y)
        direction = 1

    a = euclidean(np.array(left_eye), np.array(point_3rd))
    b = euclidean(np.array(right_eye), np.array(point_3rd))
    c = euclidean(np.array(right_eye), np.array(left_eye))


    if b != 0 and c != 0:
        cos_a = (b*b + c*c - a*a)/(2*b*c)
        angle = np.arccos(cos_a)
        angle = (angle * 180) / math.pi

        if direction == -1:
            angle = 90 - angle
        
        img = Image.fromarray(img)
        img = np.array(img.rotate(direction * angle))
    return img


if __name__ == "__main__":
    extract_faces("theAlbum")
    encode.encode()