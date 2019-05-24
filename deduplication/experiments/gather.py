# Randomly resize selected images.
# USAGE
# python gather.py --input 101_ObjectCategories --output images --csv output.csv

import argparse
import random
import shutil
import uuid

import glob
# import the necessary packages
from PIL import Image

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="input directory of images")
ap.add_argument("-o", "--output", required=True,
                help="output directory")
ap.add_argument("-c", "--csv", required=True,
                help="path to CSV file for image counts")
args = vars(ap.parse_args())

# open the output file for writing
output = open(args["csv"], "w")

# loop over the input images
for imagePath in glob.glob(args["input"] + "/*.jpg"):
    # generate a random filename for the image and copy it to
    # the output location
    filename = str(uuid.uuid4()) + ".jpg"
    shutil.copy(imagePath, args["output"] + "/" + filename)

    # there is a 1 in 500 chance that multiple copies of this
    # image will be used
    if random.randint(0, 500) == 0:
        # initialize the number of times the image is being
        # duplicated and write it to the output CSV file
        numTimes = random.randint(1, 8)
        output.write("%s,%d\n" % (filename, numTimes))

        # loop over a random number of times for this image to
        # be duplicated
        for i in range(0, numTimes):
            image = Image.open(imagePath)

            # randomly resize the image, perserving aspect ratio
            factor = random.uniform(0.95, 1.05)
            width = int(image.size[0] * factor)
            ratio = width / float(image.size[0])
            height = int(image.size[1] * ratio)
            image = image.resize((width, height), Image.ANTIALIAS)

            # generate a random filename for the image and copy
            # it to the output directory
            adjFilename = str(uuid.uuid4()) + ".jpg"
            image.save(args["output"] + "/" + adjFilename)

# close the output file
output.close()
