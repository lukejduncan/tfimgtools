"""setup tools control"""

import re
from setuptools import setup

# TODO replace with fileread
version = "0.0.1"
reqs = ['tensorflow']

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

# TODO consider a more generic name.
# TODO replace url
# TODO pick a reasonable license
setup(
    name = "tfimgtools",
    packages = ["tfimgsort"],
    entry_points = {
        "console_scripts": ['tfimgsort = tfimgsort.tfimgsort:main']
        },
    version = version,
    description = "A tool for sorting images given a tensorflow model.",
    classifiers = [
      'Development Status :: 1 - Planning',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: End Users/Desktop',
      'License :: Other/Proprietary License',
      'Programming Language :: Python :: 3 :: Only',
      'Topic :: Multimedia :: Graphics',
      'Topic :: Utilities'
     ]
    long_description = long_descr,
    install_requires=reqs,
    author = "Luke Duncan",
    author_email = "lduncan@gmail.com",
    url = "http://www.example.com",
    )
