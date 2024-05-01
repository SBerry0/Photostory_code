import os
import pickle

import numpy as np
from cv2 import imread
from PIL import Image
from sklearn.cluster import DBSCAN

import constants

METRIC = "euclidean"
NUM_JOBS = -1
MIN_SAMPLES = 2
EPSILON = 0.41


def cluster():
    # Extract data from previously created file
    data = pickle.loads(open(constants.PICKLE_FILENAME, "rb").read())
    print(data)
    data = np.array(data)
    encodings = [d["encoding"] for d in data]

    # Cluster encodings together
    print("Clustering...")
    clt = DBSCAN(metric = METRIC, n_jobs = NUM_JOBS, eps = EPSILON, min_samples = MIN_SAMPLES)
    clt.fit(encodings)
    print(clt.get_params())

    # Find total number of unique faces in dataset
    labelIDs = np.unique(clt.labels_)
    print(labelIDs)
    numUniqueFaces = len(np.where(labelIDs > -1)[0])
    print(f'Number of unique faces: {numUniqueFaces}')
    counter = 0
    if not os.path.isdir(constants.PEOPLE_PATH):
        os.mkdir(constants.PEOPLE_PATH)
    for labelID in labelIDs:
        print("INFO: faces for face ID: {}".format(labelID))
        idxs = np.where(clt.labels_ == labelID)[0]
        idxs = np.random.choice(idxs, size=min(25, len(idxs)), replace=False)

        imagepath = f"{constants.PEOPLE_PATH}/person{counter}"
        counter += 1
        os.mkdir(imagepath)
        for i in idxs:
            face = imread(str(data[i]["imagePath"]))
            h, w, _ = face.shape
            face = face[:,:,::-1]
            save = Image.fromarray(face)
            save.save(f"{imagepath}/{w}{h}_faces.jpg")

if __name__ == "__main__":
    cluster()