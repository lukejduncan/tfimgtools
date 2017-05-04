import argparse
import tensorflow as tf

parser = argparse.ArgumentParser(description='Classifies images using a tensorflow based classifier')

# TODO:
# - CSV
# - Sort per animal
# - Sort all animals


### CLI Interface
parser.add_argument("unsorted-dir", type=str)
parser.add_argument("--model-dir", help="The directory that contains the model you want to use.  Defaults to `model`", type=str)
parser.add_argument("--csv", help="When classifying the images writes a csv file of the results", action='store_true')
parser.add_argument("--singleclass", help="This is the default Sorting Scheme. Performs binary classification on the images as the specified class. The results are tiered into folders based on confidence of result. You must choose multiclass or singleclass but not both.", type=str)
parser.add_argument("--multiclass", help="Performs multiclass classification, sorting the input directory into the most likely class. You must choose multiclass or singleclass but not both.")

args = parser.parse_args()

LABELS_FILE = 'FOO'

### AUX Methods
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
  with tf.Session as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)

    with open(LABELS_FILE) as f:
      labels = f.read().splitlines()

  return (predictions, labels)

### Driver
#create_graph(args.model_dir)


# Load the model
# Load the list of images
# iterate across them, calling classify
# delegate the results

