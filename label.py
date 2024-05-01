# label.py for Photostory by Sohum Berry
import glob
import os
import sys  # For tests
from collections import defaultdict

import exifread
from geopy.geocoders import Nominatim
from GPSPhoto import gpsphoto

import scraper
import captioning

UNKNOWN = "0, 0"
IMAGE_PATH = "results/allImages/image"
# PURPOSE: Organize all collected data into iterable lists and dictionaries and also locate each image and group

# Checklist: age(refine), common objects/landmarks in image, relationship to perspective, emotions of each person
def label(input_album):
	images = list(filter(os.path.isfile, glob.glob(input_album + "/*")))
	print("\nGetting days...")
	days = get_days(input_album)
	captions = captioning.captionImages(input_album)
	# turn days into a list containing each day (getDays()), each image in the day (getDays()), and who is in the images with each other (connect())
	people_faces = []
	humans = list(filter(os.path.isdir, glob.glob("results/people" + "/*")))
	people = [os.path.basename(i) for i in humans]
	for person in humans:
		people_faces.extend(list(filter(os.path.isfile, glob.glob(person + "/*"))))
	for i in range(len(days)):
		day = days[i].copy()
		print("\nDay " + str(i), end="\n\n")
		for coord, value in day.items():
			for j in range(len(value)):
				image = value[j]
				index = images.index(image)
				together = match(index=index, people_list=people_faces)					
				value[j] = {image: together}
				print(image)
				print(captions[image])
				print("In image" + str(index) + " " + str(together) + " is/are together")
			days[i][locate(coord)] = days[i].pop(coord)
	print()
	print(days)
	
	perspective = ""
	age = 25
	while True:
		while True:
			print(f"\n{people}")
			perspective = input("Who's perspective should the Photostory be from? ")
			if len(perspective.split()) == 1:
				perspective.capitalize
				break
			else:
				print("Please enter only the first name")
		if perspective.lower() in people:
			age = scraper.findAge(perspective.lower())
			break
		else:
			print(f"{perspective} does not appear in the album")
	return days, perspective, age, captions


# Calculate how many days the album spans and return a list of each day with the images of the day in each one
def get_days(input_album):
	# Create a list of the images in the album
	images = list(filter(os.path.isfile, glob.glob(input_album + "/*")))
	
	# Layer 1: Grouping images by date
	images.sort(key=os.path.getmtime)
	# Create a list of dictionaries containing each image and it's date of creation
	dictlist = []
	for image in images:
		dated, _ = get_date(image)
		dictlist.append(dict(image_name = image, date = dated))
	# Group the images based on the attatched date
	d = defaultdict(list)
	for item in dictlist:
		d[item["date"]].append(item)
	# Remove the dates to leave only the names in their sub lists
	days = list(d.values())
	for i in range(len(days)):
		day = days[i]
		for j in range(len(day)):
			item = day[j]
			day[j] = item["image_name"]
	print(days)
	print()
	
	# Layer 2: Location
	for i in range(len(days)):
		day = days[i]
		daylist = []
		for j in range(len(day)):
			img = day[j]
			exact, approx = get_coords(img)
			daylist.append(dict(image_name = img, coord = approx))

		dd = defaultdict(list)
		for item in daylist:
			dd[item["coord"]].append(item)
		newday = {}
		values = []
		# Potential problem: this will put all locations in the same area even if it is at a different time. (ex. I go home, then some place, then back home, the two home photos will be grouped together)
		for key, value in dd.items():
			for item in value:
				values.append(item["image_name"])
			newday[key] = values[:]
			values.clear()
		days[i] = newday
	print(days)
	return days


# Convert longitude and lattitude coordinates into the name of the specified place
def locate(coord):
	if coord != UNKNOWN:
		locator = Nominatim(user_agent="Photostory")
		location = locator.reverse(coord)
		return location.raw["display_name"]
	return "Unknown"


def get_coords(img_path):
	data = gpsphoto.getGPSData(os.getcwd() + f'\\{img_path}')
	if "Latitude" in data and "Longitude" in data:
		approx_lat = round(data["Latitude"], 4)
		approx_long = round(data["Longitude"], 4)
		return str(data["Latitude"]) + ", " + str(data["Longitude"]), str(approx_lat) + ", " + str(approx_long)
	else:
		return UNKNOWN, UNKNOWN


# Get only the date and the full date of an image and convert into an integer for comparisons
def get_date(image):
	with open(image, 'rb') as fh:
		tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
		dateTaken = tags["EXIF DateTimeOriginal"]
	full_date_str = str(dateTaken)
	date_str = full_date_str[:10]
	date_num = int("".join(c for c in date_str if c.isdigit()))
	full_date_num = int("".join(c for c in full_date_str if c.isdigit()))
	return date_num, full_date_num


# Convert the date into an into for comparisons to sort
def sortDate(image):
	_, full_date_num = get_date(image)
	date_str = str(full_date_num)
	date_num = int("".join(c for c in date_str if c.isdigit()))
	return date_num


# Connect people with images to tell who was with who
# Input the the index of the image I have to search for in allImages
def match(index: int, people_list):
	# print(f"People list: {people_list}")
	faces = list(filter(os.path.isfile, glob.glob(IMAGE_PATH + str(index) + "/*")))
	together = []
	length = len(faces)
	counter = 0
	if length == 0:
		return tuple()
	for face in faces:
		for item in people_list:
			if os.path.basename(face) == os.path.basename(item):
				counter += 1
				together.append(str(os.path.basename(os.path.dirname(item))).capitalize())
				if counter == length:
					break
	return tuple(together)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("USAGE: main.py (path to input album)")
		sys.exit()
	label(input_album=sys.argv[1])