from copy import deepcopy
import json
try:
	import unittest.mock as mock
except ImportError:
	import mock
import sys
if sys.version_info[:2] < (2, 7):
	import unittest2 as unittest
else:
	import unittest

from clevertimapi.session import Session
from clevertimapi.opportunity import Opportunity
from clevertimapi.task import Task


class TestOpportunity(unittest.TestCase):

	def setUp(self):
		self.maxDiff = None
		self.session = Session('API_KEY')
