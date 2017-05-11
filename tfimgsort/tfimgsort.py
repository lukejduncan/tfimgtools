import os
import sys
import argparse
import numpy as np
import tensorflow as tf
import ntpath
from functools import reduce
from .util import *
from .tfutil import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

ERROR_DIR = 'error'

confidence_intervals = [0.9, 0.7, 0.5, 0.0]
confidence_dirs = ['high confidence', 'confident', 'low confidence', 'negative']

def sort_multiclass(img, predictions, labels, directory):
  # Take precitions
  # Move image to top scoring label
  idx = np.argmax(predictions)
  animal = labels[idx]
  animal_dir = os.path.join(directory, animal)
  mv(img, animal_dir)

## TODO decide these based on PR Curve, make configurable
def sort_singleclass(img, predictions, target, labels, directory):
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

def main():
  parser = argparse.ArgumentParser(description='Classifies images using a tensorflow based classifier')

  parser.add_argument("unsorted", type=str)
  parser.add_argument("--model-dir", help="The directory that contains the model you want to use.  Defaults to `model`", type=str)
  parser.add_argument("--csv", help="When classifying the images writes the results to a given csv file", type=str)
  parser.add_argument("--singleclass", help="This is the default Sorting Scheme. Performs binary classification on the images as the specified class. The results are tiered into folders based on confidence of result. You must choose multiclass or singleclass but not both.", type=str)
  parser.add_argument("--multiclass", help="Performs multiclass classification, sorting the input directory into the most likely class. You must choose multiclass or singleclass but not both.", action='store_true')
  parser.add_argument("--output-dir", help="The directory to output single or multiclass sorting. Defaults to 'classifications'", type=str)

  args = parser.parse_args()

  model_file = os.path.join(args.model_dir, 'output_graph.pb')
  labels_file = os.path.join(args.model_dir, 'output_labels.txt')
  output_dir = args.output_dir if args.output_dir else 'classifications'

  if args.singleclass and args.multiclass:
    print("Please use singleclass or multiclass, but not both.  See --help for details on available options.")
    sys.exit(1)

  run(args.unsorted, args.csv, args.singleclass, args.multiclass, model_file, labels_file, output_dir, ERROR_DIR)

def run(unsorted_imgs, csv, singleclass, multiclass, model_file, labels_file, output_dir):
  create_graph(model_file)
  imgs = ls(unsorted_imgs)

  with open(labels_file) as f:
    labels = f.read().splitlines()

  if csv:
    csv_file = open(csv, 'w')
    csv_file.write(stringify(labels))

  if singleclass:
    setup_dirs(confidence_dirs + [ERROR_DIR], output_dir)

  if multiclass:
    setup_dirs(labels + [ERROR_DIR], output_dir)

  for img in imgs:
    try:
      predictions = classify(img)
    except:
      error_path = os.path.join(output_dir, ERROR_DIR)
      mv(img, error_path)
      print("There was a problem classifying %s.  It has been moved to the directory %s" % (img, error_path))
      continue

    if csv:
      write_csv(csv_file, predictions)

    if singleclass:
      sort_singleclass(img, predictions, singleclass, labels, output_dir)
    elif multiclass:
      sort_multiclass(img, predictions, labels, output_dir)

  if csv:
    csv_file.close()

if __name__ == '__main__':
  main()
