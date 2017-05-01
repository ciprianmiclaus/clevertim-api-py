from clevertimapi.session import Session
# from clevertimapi.case import Case
# from clevertimapi.task import Task
# try:
#    import unittest.mock as mock
# except ImportError:
#    import mock
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')
