# name.py for Photostory by Sohum Berry
# TODO:
# Allow for more than jpg images

import os
import shutil

import cv2
import psutil
from PIL import Image

import constants

# PURPOSE: Get the naming input from the user and rename the folder to it

def name_all():
    print("NAMING PEOPLE")
    shutil.rmtree(constants.PEOPLE_PATH + "/person0")
    people = os.listdir(constants.PEOPLE_PATH)
    # For every person in the people directory...
    for item in people:
        print(f"ITEM: {item}")
        if os.path.isdir(constants.PEOPLE_PATH + "/" + item):
            person = os.listdir(constants.PEOPLE_PATH + "/" + item)
            # Take the largest image...
            img = max(person, key=lambda x: get_img_size(x, item))
            print(f"PERSON: {person}")
            # Load the image and present it
            # shouldn't be used, .open() is indended for testing purposes
            image = Image.open(os.path.join(constants.PEOPLE_PATH, item, img))
            image.show()
            # Request the name
            while True:
                name = input("What is this person's name? ")
                name = name.lower()
                if len(name.split()) == 1:
                    break
                else:
                    print("Please input only their first name")
            # Kill the image
            for proc in psutil.process_iter():
                if proc.name() == "Microsoft.Photos.exe":
                    proc.kill()
                    break
            path_name = f"{constants.PEOPLE_PATH}/{name}"
            # And rename directory containing names to the file, if the user names someone twice, add the photos to the named album instead.
            if not os.path.isdir(path_name):
                os.mkdir(path_name)
            for f in person:
                path_item = f"{constants.PEOPLE_PATH}/{item}/{f}"
                print(path_item)
                print("Moving files")
                if name.lower() != "unknown":
                    item_image = cv2.imread(path_item)
                    item_image = item_image[:,:,::-1]
                    save = Image.fromarray(item_image)
                    print(f"Saving to: {path_name}")
                    h, w, _ = item_image.shape
                    save.save(f"{path_name}/{w}{h}_faces.jpg")
                os.remove(os.path.join(constants.PEOPLE_PATH, item, f))
            os.rmdir(os.path.join(constants.PEOPLE_PATH, item))
    if os.path.isdir(constants.PEOPLE_PATH + "/unknown"):
        os.rmdir(constants.PEOPLE_PATH + "/unknown")

def get_img_size(path, item):
    width, height = Image.open(os.path.join(constants.PEOPLE_PATH, item, path)).size
    return width*height

if __name__ == "__main__":
    name_all()