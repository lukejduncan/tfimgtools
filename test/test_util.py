import os
import unittest
import random
import shutil

from tfimgsort.util import setup_dirs

ROOT_DIR = '/tmp/tfimgsort/testutil'


class TestUtil(unittest.TestCase):

    def test_setup_dirs(self):
        namespace = str(random.randint(1, 100))
        path = os.path.join(ROOT_DIR, namespace)

        self.assertFalse(os.path.isdir(path))

        labels = ['a', 'b', 'c']
        setup_dirs(labels, path)

        self.assertTrue(os.path.isdir(path))

        for label in labels:
            full_path = os.path.join(path, label)
            self.assertTrue(os.path.isdir(full_path))

        shutil.rmtree(path)


if __name__ == '__main__':
    unittest.main()
