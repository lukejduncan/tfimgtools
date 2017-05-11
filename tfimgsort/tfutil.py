import os
import sys
import numpy as np
import tensorflow as tf
import ntpath
from functools import reduce

graph_created = False

def create_graph(file):
  global graph_created
  if graph_created:
    return

  graph_created = True
  with tf.gfile.FastGFile(file, 'rb') as f:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(f.read())
      _ = tf.import_graph_def(graph_def, name='')

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
