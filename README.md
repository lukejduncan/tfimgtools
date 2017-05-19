# tfimgtools

tfimgtools is a set of CLI tools for using and evaluating image classifier models built using TensorFlow.

If you want to contribute, be sure to check out the (project wiki)[https://github.com/lukejduncan/tfimgtools/wiki]

# Installation

## Versioning
This project uses [semantic versioning](http://www.semver.org).  Any version < 1.0.0 are considered
development versions and are subject to backwards incompatible changes.

## Vagrant (recommended for development)
Primary development is done using Vagrant for environment isolation.

Assuming you have Vagrant installed the following will get you up and
running, including a Jupyter environment for exploration.

```shell
vagrant up
vagrant ssh
```

## pip (recommended for end-users)

```shell
pip3 install tfimgtools

tfimgsort --help
```

## venv

```shell
virtualenv --python=/usr/bin/python3 venv
source venv/bin/activate
pip3 install -e .
```

# Included Tools

## tfimgsort

A tool for using a given image classification model to sort
a directory of images into their classes.

### Single Class Classification

The `--singleclass` option does binary classification with 3 different
positive thresholds

Example invocation classifying images as is an elephant or not:

```shell
tfimgsort /path/to/unsorted/images --singleclass elephant --model-dir /path/to/model --output-dir /path/to/write
```

As a result, images will be move from `/path/to/unsorted/images` to `/path/to/write/classification` with the following structure:

```shell
classification/
├── high confidence
├── confident
├── low confidence
├── negative
└── error
```

Each directory is determined by a threshold that is provided at the command line.  See `tfimgsort --help` for full details.

### Multi Class Classification

The `--multiclass` option does multiclass classification with an arbitrary number of classes.
The top recommended class is choosen as the predicted class.

Example invocation classifying images as multiple classes:

```shell
tfimgsort /path/to/unsorted/images --multiclass --model-dir /path/to/model --output-dir /path/to/write
```

The resulting classifications are written in the following structure:

```shell
classification/
├── class 1
├── class 2
├── ...
├── class n
└── error
```

### Csv Generation

The `--csv` option will output a csv file with the predicted values for each class.  It can be used on it's own, on in conjuction
with either `--singleclass` or `--multiclass` options.

Example invocation done in addition to single class classification:

```shell
tfimgsort /path/to/unsorted/images --singleclass elephant --model-dir /path/to/model --output-dir /path/to/write --csv /path/to/write/csv
```

### Model Files

To run any of the classification methods, you need to have a pre-existing TensorFlow model.  The only requirement is that the model
consumes jpeg image files, outputs softmax scores of the given classes, and a mapping exists from those scores to human readable
classes.

The simplest way to do this is to either use the provided Google V3 Inception ImageNet classifier, or to retrain it with your
preferred classes.  You can find examples of how to do this in the TensorFlow docs in the further reading section.

If you follow the transfer learning guide it will output a trained network as the file `output_graph.pb` and map from the
the output layer to human readable labels as the file `output_labels.txt`.  The `--model-dir` option should point to a directory
with these two files for classification.

#### Further Reading
- [Intro to Inception V3](https://www.tensorflow.org/tutorials/image_recognition)
- [Transfer Learning with Inception](https://www.tensorflow.org/tutorials/image_retraining)

# License

This project is licensed under the MIT License.  You can find more information in the `LICENSE` file or at [https://choosealicense.com/licenses/mit/](https://choosealicense.com/licenses/mit/)
