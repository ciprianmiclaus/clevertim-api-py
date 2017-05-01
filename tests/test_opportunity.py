from clevertimapi.session import Session
from clevertimapi.opportunity import Opportunity
from clevertimapi.task import Task
from clevertimapi.user import User
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


class TestOpportunity(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')

        self.opp1 = {
            'name': 'Opportunity 1',
            'description': 'Clevertim is a great company. They do software.',
            # 'cust': 1,
            'leadUser': 2,
            'currency': 'EUR',
            'value': '1000.50',
            'status': 'Won',
            'tags': ['tag1', 'tag2', 'tag3'],
            'tasks': [1, 2],
        }
        self.opp2 = {
            'id': 445,
            'name': 'Opportunity 2',
            'description': 'Some Ltd. is fantastic. Its customer support is unlike anything out there.',
            # 'cust': 2,
            'leadUser': 3,
            'currency': 'GBP',
            'value': '652.75',
            'status': 'Lost',
            'tags': ['othertag1', 'othertag2', 'othertag3'],
            'tasks': [3, 4, 2],
        }

    @mock.patch('requests.get')
    def test_load_opportunity(self, mockRequestsGET):
        c1 = deepcopy(self.opp1)
        c1['id'] = 445

        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps({
            'status': 'OK',
            'content': [
                c1
            ]
        })
        mockRequestsGET.return_value = response

        c = Opportunity(self.session, key=445)
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)
        self.assertEqual(c.name, 'Opportunity 1')
        self.assertEqual(c.description, 'Clevertim is a great company. They do software.')

        self.assertEqual(c.currency, 'EUR')
        self.assertEqual(c.value, '1000.50')
        self.assertEqual(c.status, 'Won')

        self.assertEqual(c.tags, ['tag1', 'tag2', 'tag3'])

        self.assertIsInstance(c.lead_user, User)
        self.assertEqual(c.lead_user.key, 2)

        self.assertTrue(all(isinstance(t, Task) for t in c.tasks))
        self.assertEqual([t.key for t in c.tasks], [1, 2])

    @mock.patch('requests.post')
    def test_add_new_opportunity(self, mockRequestsPOST):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps({
            'status': 'OK',
            'content': [
                {
                    'id': 3456
                }
            ]
        })
        mockRequestsPOST.return_value = response

        c = Opportunity(self.session)
        c.name = 'Opportunity 1'
        c.description = 'Clevertim is a great company. They do software.'
        c.currency = 'EUR'
        c.value = '1000.50'
        c.status = 'Won'

        c.tags = ['tag1', 'tag2', 'tag3']

        c.lead_user = User(self.session, key=2, lazy_load=True)

        c.tasks = [Task(self.session, key=1, lazy_load=True), Task(self.session, key=2, lazy_load=True)]

        self.assertTrue(c.is_new())
        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 3456)

        args = mockRequestsPOST.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Opportunity.ENDPOINT)
        self.assertEqual(data, self.opp1)

    @mock.patch('requests.put')
    @mock.patch('requests.get')
    def test_edit_existing_opportunity(self, mockRequestsGET, mockRequestsPUT):
        c1 = deepcopy(self.opp1)
        c1['id'] = 445

        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps({
            'status': 'OK',
            'content': [
                c1
            ]
        })
        mockRequestsGET.return_value = response
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps({
            'status': 'OK',
            'content': [
                {
                    'id': 445
                }
            ]
        })
        mockRequestsPUT.return_value = response

        c = Opportunity(self.session, key=445)
        c.name = 'Opportunity 2'
        c.description = 'Some Ltd. is fantastic. Its customer support is unlike anything out there.'
        c.currency = 'GBP'
        c.value = '652.75'
        c.status = 'Lost'

        c.lead_user = User(self.session, key=3, lazy_load=True)

        c.tags = ['othertag1', 'othertag2', 'othertag3']

        c.tasks = [Task(self.session, key=3, lazy_load=True), Task(self.session, key=4, lazy_load=True), Task(self.session, key=2, lazy_load=True)]

        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)

        args = mockRequestsPUT.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Opportunity.ENDPOINT + '/445')
        self.assertEqual(data, self.opp2)
