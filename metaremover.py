import argparse
import pyexiv2
from PIL import Image
from PIL.ExifTags import TAGS

def ClearAllMetadata(imgname, preserve):
	metadata = pyexiv2.ImageMetadata(imgname)
	metadata.read()
	metadata.clear()
	metadata.write(preserve)

def ModifyMode(imgname, preserve):
	metadata = pyexiv2.ImageMetadata(imgname)
	metadata.read()
	for key, value in metadata.iteritems():
		print key, value.raw_value
	modkey = raw_input("Key to modify (q to Quit): ")
	while modkey != 'q':
		print "Editing:" + str(metadata[modkey].raw_value)
		modvalue = raw_input("New Value: (q to Quit): ")
		if modvalue == 'q':
			break
		metadata[modkey].raw_value = str(modvalue)
		modkey = raw_input("Key to modify (q to Quit): ")
	metadata.write(preserve)

def ExtractMode(imgname, export):
	try:
		metaData = {}
		imgFile = Image.open(imgname)
		print "Getting metadata..."
		info = imgFile._getexif()
		if info:
			for (tag, value) in info.items():
				tagname = TAGS.get(tag, tag)
				metaData[tagname] = value
				if not export:
					print tagname, value
			if export:
				print "Outputting to file..."
				f = open(export, "w+")
				for (tagname, value) in metaData.items():
					f.write(str(tagname)+"\t" + str(value) + "\n")
				f.close()
		imgFile.close()
		
	except:
		print "Failed to get metadata"

def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("img", help = "Image file to manipulate")
	parser.add_argument("--clear", "-c", 
		help = "Clear all metadata from file", action = "store_true")
	parser.add_argument("--preserve", "-p", help = "Preserve image modified date", action = "store_true")
	parser.add_argument("--export", "-e", help = "dump data to file")
	args = parser.parse_args()
	if args.img:
		if args.clear:
			ClearAllMetadata(args.img, args.preserve)
		elif args.export:
			ExtractMode(args.img, args.export)
		elif args.preserve: 
			ModifyMode(args.img, args.preserve)
		else:
			ExtractMode(args.img, args.export)
	else:
		print parser.usage
if __name__ == "__main__":
        Main()

