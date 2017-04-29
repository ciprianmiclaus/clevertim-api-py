import os
from setuptools import setup, find_packages

current_dir = os.path.abspath(os.path.dirname(__name__))
with open(os.path.join(current_dir, 'README.md'), 'rb') as f:
	long_description = f.read()


import unittest
def unittest_discover_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite
	
	
setup(
	name = 'clevertimapi',
	version = '0.0.1',
	description = 'Clevertim CRM Python API',
	long_description = long_description,
	url = 'https://github.com/ciprianmiclaus/clevertim-api-py',
	author = 'Ciprian Miclaus',
	author_email = 'ciprianm@gmail.com',
	license = 'BSD3',
	
	classifiers = [
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Developers',
		'Topic :: Software Development :: API',

		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
	],

	keywords = 'Clevertim CRM contact management API development',

	packages = find_packages(),
	install_requires = ['requests'],

	test_suite = 'setup.unittest_discover_test_suite',

)