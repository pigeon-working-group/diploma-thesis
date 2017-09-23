from distutils.spawn import find_executable
from subprocess import call
from os.path import isdir, isfile
from os import mkdir, listdir
from hashlib import md5 as md5_
from json import load, dump
from mimetypes import guess_type

PAPER = "paper.tex"
QUICK_PAPER = "quick_paper.tex"
IMAGES_LOCATION = "images/"
RESIZED_IMAGES_LOCATION = "images_resized/"
RESIZED_IMAGES_HASHES = RESIZED_IMAGES_LOCATION + "hashes.json"
IMAGEMAGICK_INSTALLED = True if find_executable("mogrify") else False

QUALITY = 20
RESIZE_PERCENTAGE = 30

def md5(fname):
	""" 
	https://stackoverflow.com/a/3431838/4739690

	md5 is percise enough for this use-case, this isn't crypto after all ;)
	"""		
	hash_md5 = md5_()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()


def reduce_image_quality(src, dest):
	""" 
	Reduce image quality to speed up latex rendering
	"""	
	return call([
		"mogrify", "-quality", str(QUALITY), 
		"-resize", str(RESIZE_PERCENTAGE) + "%", "-path", dest, src
	])


def patch_graphicspath(src, graphics_path, dest):
	""" 
	Patch graphicspath to point to resized images location 
	"""
	tmp = ""

	for line in open(src, "r"):
		if line.startswith("\graphicspath{"):
			tmp += "\graphicspath{{%s/}}\n" % graphics_path
		else:
			tmp += line	
	open(dest, "w").write(tmp)


def is_image(path):
	"""
	Try to guess if file is an images based upon it's mimetype
	"""
	type_ = guess_type(path)[0]
	if type_ != None:
		return type_.startswith("image/")
	return False


def dump_image_hash_index(folder, dest):
	hashes = {}

	folder = folder + "/" if not folder.endswith("/") else folder

	for file in listdir(folder):
		if is_image(file):
			hashes[file] = md5(folder + file)	

	dump(hashes, open(dest, "w"))



if IMAGEMAGICK_INSTALLED:
	if not isdir(RESIZED_IMAGES_LOCATION):
		mkdir(RESIZED_IMAGES_LOCATION)
	if not isfile(RESIZED_IMAGES_HASHES):
		dump_image_hash_index(IMAGES_LOCATION, RESIZED_IMAGES_HASHES)

	hashes = load(open(RESIZED_IMAGES_HASHES, "r"))

	for file in listdir(IMAGES_LOCATION):
		if is_image(IMAGES_LOCATION + file):
			if not isfile(RESIZED_IMAGES_LOCATION + file):
				print("New image: '%s'" % file)
				reduce_image_quality(IMAGES_LOCATION + file, 
					RESIZED_IMAGES_LOCATION)
			else:
				if hashes[file] != md5(IMAGES_LOCATION + file):
					print("Changes in image: '%s'" % file)
					reduce_image_quality(IMAGES_LOCATION + file, 
						RESIZED_IMAGES_LOCATION)


	patch_graphicspath(PAPER, RESIZED_IMAGES_LOCATION, QUICK_PAPER)
	dump_image_hash_index(IMAGES_LOCATION, RESIZED_IMAGES_HASHES)
else:
	print("ImageMagick not installed, can't resize.")
	exit(1)