from copy import deepcopy
import json
import mock
import unittest

import sys
sys.path.append('../src')

from session import Session
from case import Case
from task import Task


class TestCase(unittest.TestCase):

	def setUp(self):
		self.maxDiff = None
		self.session = Session('API_KEY')
