from distutils.spawn import find_executable
from subprocess import check_call
from os.path import isdir, isfile
from os import mkdir, listdir

PAPER = "paper.tex"
QUICK_PAPER = "quick_paper.tex"
IMAGES_LOCATION = "images"
RESIZED_IMAGES_LOCATION = "images_resized"
IMAGEMAGICK_INSTALLED = True if find_executable("convert") else False

out = ""

if IMAGEMAGICK_INSTALLED:
	if not isdir(RESIZED_IMAGES_LOCATION):
		mkdir(RESIZED_IMAGES_LOCATION)

	for image in listdir(IMAGES_LOCATION):
		if not isfile("{}/{}".format(RESIZED_IMAGES_LOCATION, image)):
			# Not patient enough to convert command to list
			if image.lower().endswith((".jpeg", ".png", ".jpg")):
				check_call("mogrify -quality 50 -resize 50% -path {} {}/{}".format(
					RESIZED_IMAGES_LOCATION, IMAGES_LOCATION, image), shell=True)

	for line in open(PAPER, "r"):
		if line.startswith("\graphicspath{"):
			out += "\graphicspath{{%s/}}\n" % RESIZED_IMAGES_LOCATION
		else:
			out += line

	open(QUICK_PAPER, "w").write(out)

else:
	stderr.write("ImageMagick not installed, can't resize.", file=stderr)
