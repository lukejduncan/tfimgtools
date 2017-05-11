import os
import sys
import ntpath
from functools import reduce

def stringify(nplist):
  string = reduce((lambda x, y: str(x) + ',' + str(y)), nplist)
  string += '\n'
  return string

def write_csv(csv_file, predictions):
  csv_file.write(stringify(predictions))

def ls(img_dir):
  return [os.path.join(img_dir, img) for img in os.listdir(img_dir)]

def mv(from_file, to_dir):
  base = ntpath.basename(from_file)
  os.rename(from_file, os.path.join(to_dir, base))

def setup_dirs(labels, directory):
  if not os.path.isdir(directory):
    os.makedirs(directory)

  if os.path.isdir(directory):
    if len(os.listdir(directory)):
      print("ERROR: %s needs to be an empty directory." % (directory))
      sys.exit(1)

  sub_dirs = list(map((lambda x: os.path.join(directory, x)), labels))

  for d in sub_dirs:
    os.makedirs(d)
