from setuptools import setup

setup(name='py_utils',
      version='0.0.1',
      description='Python utilities',
      url='http://github.com/asundaresan/py_utils',
      author='Aravind Sundaresan',
      author_email='asundaresan@gmail.com',
      license='GPLv3',
      packages=['py_utils'],
			scripts=["bin/mortgage.py"],
      zip_safe=False)

