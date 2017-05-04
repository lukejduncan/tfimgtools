import argparse

parser = argparse.ArgumentParser(description='Classifies images using a tensorflow based classifier')

# TODO:
# - CSV
# - Sort per animal
# - Sort all animals

parser.add_argument("unsorted-dir", type=str)
parser.add_argument("--model-dir", help="The directory that contains the model you want to use.  Defaults to `model`", type=str)
parser.add_argument("--csv", help="When classifying the images writes a csv file of the results", action='store_true')
parser.add_argument("--singleclass", help="This is the default Sorting Scheme. Performs binary classification on the images as the specified class. The results are tiered into folders based on confidence of result. You must choose multiclass or singleclass but not both.", type=str)
parser.add_argument("--multiclass", help="Performs multiclass classification, sorting the input directory into the most likely class. You must choose multiclass or singleclass but not both.")

args = parser.parse_args()
