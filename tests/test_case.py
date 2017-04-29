from copy import deepcopy
import json
import mock
import unittest

from clevertimapi.session import Session
from clevertimapi.case import Case
from clevertimapi.task import Task


class TestCase(unittest.TestCase):

	def setUp(self):
		self.maxDiff = None
		self.session = Session('API_KEY')
