from copy import deepcopy
import json
import mock
import unittest

import sys
sys.path.append('../src')

from session import Session
from opportunity import Opportunity
from task import Task


class TestOpportunity(unittest.TestCase):

	def setUp(self):
		self.maxDiff = None
		self.session = Session('API_KEY')
