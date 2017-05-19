"""setup tools control"""

from setuptools import setup

version = "0.0.8"
reqs = ['tensorflow']


setup(
    name="tfimgtools",
    packages=['tfimgsort', 'test'],
    setup_requires=['flake8'],
    test_suite='test',
    entry_points={
        "console_scripts": ['tfimgsort = tfimgsort.tfimgsort:main']
        },
    version=version,
    description="A tool for sorting images given a tensorflow model.",
    long_description="A tool for sorting images given a tensorflow model.",
    classifiers=[
      'License :: OSI Approved :: MIT License',
      'Development Status :: 1 - Planning',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: End Users/Desktop',
      'License :: Other/Proprietary License',
      'Programming Language :: Python :: 3 :: Only',
      'Topic :: Multimedia :: Graphics',
      'Topic :: Utilities'
     ],
    keyword='computer-vision tensorflow cli',
    license='MIT',
    install_requires=reqs,
    author="Luke Duncan",
    author_email="lukejduncan@gmail.com",
    url='https://github.com/lukejduncan/tfimgtools',
    )
