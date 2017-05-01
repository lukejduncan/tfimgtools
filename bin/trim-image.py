import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("image", help="the image to modify")
parser.add_argument("--header-trim", help="number of pixels to remove from the top of the image", type=int)
parser.add_argument("--footer-trim", help="number of pixels to remove from the bottom of the image", type=int)
args = parser.parse_args()

img = Image.open(args.image)
width = img.size[0]
height = img.size[1]

left_x = 0
left_y = 0

right_x = width 
right_y = height

if args.header_trim:
	left_y = args.header_trim

if args.footer_trim:
	right_y = height - args.footer_trim

img2 = img.crop((left_x, left_y, right_x, right_y))
img2.save("trimmed-" + args.image)
