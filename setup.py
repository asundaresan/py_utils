#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='py_utils',
      version='0.1.0',
      description='Python utilities',
      url='http://github.com/asundaresan/py_utils',
      author='Aravind Sundaresan',
      author_email='asundaresan@gmail.com',
      license='GPLv3',
      packages=['mortgage','file_utils'],
      scripts=[
        "bin/mortgage_table.py",
        "bin/check_duplicates.py"
        "file_utils/bin/filter_images.py"
        ],
      zip_safe=False
      )

