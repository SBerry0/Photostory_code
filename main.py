# main.py for Photostory by Sohum Berry
import glob
import os
import shutil
import sys

import cluster
import encode
import extract
import generator
import label
import name

def removeDuplicates(input_album):
	images = list(filter(os.path.isfile, glob.glob(input_album + "/*")))
	prev_date = 0
	shutil.rmtree("input")
	os.mkdir("input")
	for image in images:
		print(os.path.getmtime(image))

		print(abs(os.path.getmtime(image) - prev_date))
		if abs(os.path.getmtime(image) - prev_date) > 6:
			print("copying")
			prev_date = os.path.getmtime(image)
			shutil.copy2(image, "input/" + str(os.path.basename(image)))


if __name__ == "__main__":
	# Make sure an input album is inputted
	# TODO: Check if the album exists
	if len(sys.argv) != 2:
		print("USAGE: main.py (path to input album)")
		sys.exit()
	input_album = sys.argv[1]
	if len(list(filter(os.path.isfile, glob.glob(input_album + "/*")))) == 0:
		print("That album doesn't exist!")
		sys.exit()
	removeDuplicates(input_album)
	# Restart and delete already created data (for testing)
	if os.path.isdir("results"):
		shutil.rmtree("results")
	# Create directories for data to go to
	print("Creating dirs")
	os.mkdir("results")
	os.mkdir("results/allImages")
	os.mkdir("results/allFaces")
	os.mkdir("results/people")

	
	# scraper.createCast(input_album=input_album)
	extract.extract_faces(dir="input")
	encode.encode()
	cluster.cluster()
	name.name_all()
	storyline, character, age, captions = label.label(input_album="input")
	generator.generate(storyline=storyline, name=character, age=age, caps=captions)

