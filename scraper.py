#scraper.py for Photostory by Sohum Berry
from pathlib import Path
from deepface import DeepFace
from collections import defaultdict
import cv2
import os
import glob
from PIL import Image

# PURPOSE: Remove every face from the album and organize in folders

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# The main function that takes all of the faces and sorts them by person in seperate directories
def createCast(input_album: str):
    scrapeFaces(folder_dir=input_album)
    
    # Now we have only the faces in a directory
    pathfaces = list(Path("results/allFaces").glob("*.jpg"))
    counter = 0
    while len(pathfaces) > 0:
        # For every face search for it in the rest of allFaces. If a face is found, delete it so there won't be doubled matches
        face = pathfaces[0]
        print("\nFACE: " + str(face))
        df = DeepFace.find(str(face), "results/allFaces", enforce_detection=False, silent = True, model_name="VGG-Face")
        identity = df[0]["identity"]
        distance = df[0]["VGG-Face_cosine"]
        iterate = 0
        imagepath = f"results/people/person{counter}"
        os.mkdir(imagepath)
        print(identity)
        for item in identity:
            if Path(item) in pathfaces:
                if distance[iterate] < 0.31:
                    print("FileName: " + item + "\nDistance: " + str(distance[iterate]))
                    iterate +=1
                    item_image = cv2.imread(str(item))
                    # Write the file with dimensions so I can trace it back to the allImages folder
                    h, w, _ = item_image.shape
                    item_image = item_image[:,:,::-1]
                    save = Image.fromarray(item_image)
                    save.save(f"{imagepath}/{w}{h}_faces.jpg")
                    print("DELETING...")
                    pathfaces.remove(Path(item))
        counter += 1

# Goes through the files in a folder and scrapes it for faces
def scrapeFaces(folder_dir: str):
    images = list(filter(os.path.isfile, glob.glob(folder_dir + "/*")))
    counter = 0
    
    # For every jpg image, lift the faces
    for image in images:
        if str(image) != str(folder_dir + "/.DS_Store"):
            print("Image: " + str(counter) + " Name: " + str(image))
            scrape(image_name=str(image), image_num=counter)
            counter += 1

# Takes all faces in the image and loads it to a folder
def scrape(image_name: str, image_num: int = 0):
    # Load the image then grayscale it for analyzing
    image = cv2.imread(str(image_name))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # A list containing each face in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.3,
        minNeighbors = 3,
        minSize = (100, 100)
    )
    # Convert from BGR to RGB for writing
    image = image[:,:,::-1]
    # Create directory to add images to
    path = f"results/allImages/image{str(image_num)}"
    os.mkdir(path)
    # Create and extract the coordinates of the face and save to directories
    for (x, y, w, h) in faces:
        roi_color = image[y:y + h, x:x + w]
        print("Face found. Saving...")
        save = Image.fromarray(roi_color)
        save.save(f"{path}/{w}{h}_faces.jpg")
        save.save("results/allFaces/" + str(w) + str(h) + '_faces.jpg')

basedir = "results/people/"

def findAge(name):
    print(f"Calculating {name.capitalize()}'s age...")
    ages = []
    images = list(Path(f"{basedir}{name}").glob("*.jpg"))
    for img in images:
        features = DeepFace.analyze(img_path = str(img), actions = ["age"], enforce_detection=False)
        age = features[0]["age"]
        ages.append(age)
    avg = sum(ages) // len(ages)
    print("Age: " + str(avg))
    return avg

def findEmotion(img_path):
    print("Attribute img path: " + str(img_path))
    emotion = "neutral"
    features = DeepFace.analyze(img_path = img_path, actions = ["emotion"], enforce_detection=False)
    emotion = features[0]["dominant_emotion"]
    print("Emotion: " + str(emotion))
    return emotion