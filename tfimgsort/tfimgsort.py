import os
import sys
import argparse
import numpy as np
import tensorflow as tf
import ntpath
from functools import reduce

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

parser = argparse.ArgumentParser(description='Classifies images using a tensorflow based classifier')

# TODO handle damaged images

### CLI Interface
parser.add_argument("unsorted", type=str)
parser.add_argument("--model-dir", help="The directory that contains the model you want to use.  Defaults to `model`", type=str)
parser.add_argument("--csv", help="When classifying the images writes the results to a given csv file", type=str)
parser.add_argument("--singleclass", help="This is the default Sorting Scheme. Performs binary classification on the images as the specified class. The results are tiered into folders based on confidence of result. You must choose multiclass or singleclass but not both.", type=str)
parser.add_argument("--multiclass", help="Performs multiclass classification, sorting the input directory into the most likely class. You must choose multiclass or singleclass but not both.", action='store_true')
parser.add_argument("--output-dir", help="The directory to output single or multiclass sorting. Defaults to 'classifications'", type=str)

args = parser.parse_args()

MODEL_FILE = os.path.join(args.model_dir, 'output_graph.pb')
LABELS_FILE = os.path.join(args.model_dir, 'output_labels.txt')
OUTPUT_DIR = args.output_dir if args.output_dir else 'classifications'
ERROR_DIR = 'error'

confidence_intervals = [0.9, 0.7, 0.5, 0.0]
confidence_dirs = ['high confidence', 'confident', 'low confidence', 'negative']

if args.singleclass and args.multiclass:
  print("Please use singleclass or multiclass, but not both.  See --help for details on available options.")
  sys.exit(1)

### AUX Methods
def stringify(nplist):
  string = reduce((lambda x, y: str(x) + ',' + str(y)), nplist)
  string += '\n'
  return string

def csv(csv_file, predictions):
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

def create_graph(file):
  with tf.gfile.FastGFile(file, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      _ = tf.import_graph_def(graph_def, name='')

# TODO: replace with argparse tensor names
def classify(img):
  answer = None

  if not tf.gfile.Exists(img):
    tf.logging.fatal('File does not exist %s', img)
    return answer

  image_data = tf.gfile.FastGFile(img, 'rb').read()

  with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)


  return predictions

def multiclass(img, predictions, labels, directory):
  # Take precitions
  # Move image to top scoring label
  idx = np.argmax(predictions)
  animal = labels[idx]
  animal_dir = os.path.join(directory, animal)
  mv(img, animal_dir)


## TODO decide these based on PR Curve, make configurable
def singleclass(img, predictions, target, labels, directory):
  global confidence_dirs
  global confidence_intervals

  idx = labels.index(target)
  prob = predictions[idx]

  expanded_dirs = [os.path.join(directory, d) for d in confidence_dirs]

  ## Assumes decreasing order
  for i in range(len(confidence_intervals)):
    if prob > confidence_intervals[i]:
      mv(img, expanded_dirs[i])
      break

### Driver
create_graph(MODEL_FILE)
imgs = ls(args.unsorted)

with open(LABELS_FILE) as f:
  labels = f.read().splitlines()

if args.csv:
  csv_file = open(args.csv, 'w')
  csv_file.write(stringify(labels))

if args.singleclass:
  setup_dirs(confidence_dirs + [ERROR_DIR], OUTPUT_DIR)

if args.multiclass:
  setup_dirs(labels + [ERROR_DIR], OUTPUT_DIR)

for img in imgs:
  try:
    predictions = classify(img)
  except:
    error_path = os.path.join(OUTPUT_DIR, ERROR_DIR)
    mv(img, error_path)
    print("There was a problem classifying %s.  It has been moved to the directory %s" % (img, error_path))
    continue

  if args.csv:
    csv(csv_file, predictions)

  if args.singleclass:
    singleclass(img, predictions, args.singleclass, labels, OUTPUT_DIR)
  elif args.multiclass:
    multiclass(img, predictions, labels, OUTPUT_DIR)

if args.csv:
  csv_file.close()
