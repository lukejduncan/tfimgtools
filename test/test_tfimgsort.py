import os
import random
import shutil
import unittest

from tfimgsort.tfimgsort import run
from tfimgsort.util import ls

MODEL_DIR = '/tmp/tfimgsort/inception_model'
ROOT_DIR = '/tmp/tfimgsort/Testtfimgsort'

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_MODEL_DIR = os.path.join(MODULE_DIR, 'resources/model')
RESOURCE_IMGS_GOOD_DIR = os.path.join(MODULE_DIR, 'resources/imgs/imgs_good')
RESOURCE_IMGS_ERROR_DIR = os.path.join(MODULE_DIR, 'resources/imgs/imgs_error')


class TestTfimgsort(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(ROOT_DIR):
            os.makedirs(ROOT_DIR)

        r = str(random.randint(1, 100000))
        self.test_dir = os.path.join(ROOT_DIR, r)

        self.output_dir = os.path.join(self.test_dir, 'output')
        os.makedirs(self.output_dir)

        self.input_dir = os.path.join(self.test_dir, 'input')
        os.makedirs(self.input_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_tfimgsort_singleclass(self):
        shutil.copyfile(os.path.join(RESOURCE_IMGS_GOOD_DIR, 'test.jpg'),
                        os.path.join(self.input_dir, 'test.jpg'))

        csv = False
        singleclass = 'elephant'
        multiclass = False
        model_file = os.path.join(RESOURCE_MODEL_DIR, 'output_graph.pb')
        labels_file = os.path.join(RESOURCE_MODEL_DIR, 'output_labels.txt')
        confidence_thresh = [0.9, 0.7, 0.5, 0.0]

        original_imgs = ls(self.input_dir)
        run(self.input_dir, csv, singleclass, multiclass, model_file,
            labels_file, confidence_thresh, self.output_dir)

        sorted_files = 0
        conf = ['high confidence', 'confident', 'low confidence', 'negative']
        for label in conf:
            p = os.path.join(self.output_dir, label)
            self.assertTrue(os.path.isdir(p), "Couldn't find %s" % (p))
            children = ls(p)
            sorted_files += len(children)

        self.assertEqual(len(original_imgs), sorted_files)

    def test_tfimgsort_error(self):
        shutil.copyfile(os.path.join(RESOURCE_IMGS_ERROR_DIR, 'test.jpg'),
                        os.path.join(self.input_dir, 'test.jpg'))

        csv = False
        singleclass = 'elephant'
        multiclass = False
        model_file = os.path.join(RESOURCE_MODEL_DIR, 'output_graph.pb')
        labels_file = os.path.join(RESOURCE_MODEL_DIR, 'output_labels.txt')
        confidence_thresh = None

        original_imgs = ls(self.input_dir)
        run(self.input_dir, csv, singleclass, multiclass, model_file,
            labels_file, confidence_thresh, self.output_dir)

        sorted_files = 0
        for label in ['error']:
            p = os.path.join(self.output_dir, label)
            self.assertTrue(os.path.isdir(p), "Couldn't find %s" % (p))
            children = ls(p)
            sorted_files += len(children)

        self.assertEqual(len(original_imgs), sorted_files)

    def test_tfimgsort_multiclass(self):
        shutil.copyfile(os.path.join(RESOURCE_IMGS_GOOD_DIR, 'test.jpg'),
                        os.path.join(self.input_dir, 'test.jpg'))

        csv = False
        singleclass = None
        multiclass = True
        model_file = os.path.join(RESOURCE_MODEL_DIR, 'output_graph.pb')
        labels_file = os.path.join(RESOURCE_MODEL_DIR, 'output_labels.txt')
        confidence_thresh = None

        original_imgs = ls(self.input_dir)
        run(self.input_dir, csv, singleclass, multiclass, model_file,
            labels_file, confidence_thresh, self.output_dir)

        sorted_files = 0
        for label in ['elephant']:
            p = os.path.join(self.output_dir, label)
            self.assertTrue(os.path.isdir(p), "Couldn't find %s" % (p))
            children = ls(p)
            sorted_files += len(children)

        self.assertEqual(len(original_imgs), sorted_files)

    def test_tfimgsort_csv(self):
        shutil.copyfile(os.path.join(RESOURCE_IMGS_GOOD_DIR, 'test.jpg'),
                        os.path.join(self.input_dir, 'test.jpg'))

        csv = os.path.join(self.test_dir, 'test.csv')
        singleclass = None
        multiclass = False
        model_file = os.path.join(RESOURCE_MODEL_DIR, 'output_graph.pb')
        labels_file = os.path.join(RESOURCE_MODEL_DIR, 'output_labels.txt')
        confidence_thresh = None

        run(self.input_dir, csv, singleclass, multiclass, model_file,
            labels_file, confidence_thresh, self.output_dir)

        self.assertTrue(os.path.isfile(csv))


if __name__ == '__main__':
    unittest.main()
