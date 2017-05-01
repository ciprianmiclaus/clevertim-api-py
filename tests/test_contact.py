from clevertimapi.session import Session
from clevertimapi.contact import Contact
from clevertimapi.company import Company
from clevertimapi.task import Task
from clevertimapi.opportunity import Opportunity
from clevertimapi.case import Case
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


class TestContact(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')

        self.contact1 = {
            'fn': 'Mike',
            'ln': 'Doodley',
            'title': 'Engineer',
            'is_company': False,
            'companyId': 999,
            'address': '199 Maverick Road',
            'city': 'London',
            'postcode': 'SW19 7BH',
            'region': 'US-FL',
            'country': 'US',
            'description': 'Mike is a great, likeable guy. He always returns my calls.',
            'email': ['mike.doodley@gmail.com', 'mike.doodley@yahoo.com'],
            'website': ['http://www.google.com', 'http://www.mikedoodley.com'],
            'tags': ['tag1', 'tag2', 'tag3'],
            'tasks': [1, 2],
            'opportunities': [100, 101, 211],
            'cases': [55, 57]
        }
        self.contact2 = {
            'id': 445,
            'fn': 'John',
            'ln': 'Rowdy',
            'title': 'CEO',
            'is_company': False,
            'companyId': 456,
            'address': '32 Bossy Lane',
            'city': 'Winchester',
            'postcode': 'WH7 8AB',
            'region': 'GB-WRL',
            'country': 'GB',
            'description': 'John is very bossy. He even lives on a bossy lane.',
            'email': ['john.rowdy@gmail.com', 'john.rowdy@yahoo.com'],
            'website': ['http://www.johnrowdy.com', 'http://www.yahoo.com'],
            'tags': ['othertag1', 'othertag2', 'othertag3'],
            'tasks': [3, 4, 2],
            'opportunities': [45, 101, 33],
            'cases': [55, 89]
        }

    @mock.patch('requests.get')
    def test_load_contact(self, mockRequestsGET):
        c1 = deepcopy(self.contact1)
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

        c = Contact(self.session, key=445)
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)
        self.assertEqual(c.first_name, 'Mike')
        self.assertEqual(c.last_name, 'Doodley')
        self.assertEqual(c.title, 'Engineer')
        self.assertEqual(c.address, '199 Maverick Road')
        self.assertEqual(c.city, 'London')
        self.assertEqual(c.postcode, 'SW19 7BH')
        self.assertEqual(c.region, 'US-FL')
        self.assertEqual(c.country, 'US')
        self.assertEqual(c.description, 'Mike is a great, likeable guy. He always returns my calls.')
        self.assertEqual(c.emails, ['mike.doodley@gmail.com', 'mike.doodley@yahoo.com'])
        self.assertEqual(c.websites, ['http://www.google.com', 'http://www.mikedoodley.com'])
        self.assertEqual(c.tags, ['tag1', 'tag2', 'tag3'])

        self.assertIsInstance(c.company, Company)
        self.assertEqual(c.company.key, 999)

        self.assertTrue(all(isinstance(t, Task) for t in c.tasks))
        self.assertEqual([t.key for t in c.tasks], [1, 2])
        self.assertTrue(all(isinstance(t, Opportunity) for t in c.opportunities))
        self.assertEqual([t.key for t in c.opportunities], [100, 101, 211])
        self.assertTrue(all(isinstance(t, Case) for t in c.cases))
        self.assertEqual([t.key for t in c.cases], [55, 57])

    @mock.patch('requests.post')
    def test_add_new_contact(self, mockRequestsPOST):
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

        c = Contact(self.session)
        c.first_name = 'Mike'
        c.last_name = 'Doodley'
        c.title = 'Engineer'
        c.address = '199 Maverick Road'
        c.city = 'London'
        c.postcode = 'SW19 7BH'
        c.region = 'US-FL'
        c.country = 'US'
        c.description = 'Mike is a great, likeable guy. He always returns my calls.'
        c.emails = ['mike.doodley@gmail.com', 'mike.doodley@yahoo.com']
        c.websites = ['http://www.google.com', 'http://www.mikedoodley.com']
        c.tags = ['tag1', 'tag2', 'tag3']

        c.company = Company(self.session, key=999, lazy_load=True)

        c.tasks = [Task(self.session, key=1, lazy_load=True), Task(self.session, key=2, lazy_load=True)]
        c.opportunities = [Opportunity(self.session, key=100, lazy_load=True), Opportunity(self.session, key=101, lazy_load=True), Opportunity(self.session, key=211, lazy_load=True)]
        c.cases = [Case(self.session, key=55, lazy_load=True), Case(self.session, key=57, lazy_load=True)]

        self.assertTrue(c.is_new())
        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 3456)

        args = mockRequestsPOST.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Contact.ENDPOINT)
        self.assertEqual(data, self.contact1)

    @mock.patch('requests.put')
    @mock.patch('requests.get')
    def test_edit_existing_contact(self, mockRequestsGET, mockRequestsPUT):
        c1 = deepcopy(self.contact1)
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

        c = Contact(self.session, key=445)
        c.first_name = 'John'
        c.last_name = 'Rowdy'
        c.title = 'CEO'
        c.address = '32 Bossy Lane'
        c.city = 'Winchester'
        c.postcode = 'WH7 8AB'
        c.region = 'GB-WRL'
        c.country = 'GB'
        c.description = 'John is very bossy. He even lives on a bossy lane.'
        c.emails = ['john.rowdy@gmail.com', 'john.rowdy@yahoo.com']
        c.websites = ['http://www.johnrowdy.com', 'http://www.yahoo.com']
        c.tags = ['othertag1', 'othertag2', 'othertag3']

        c.company = Company(self.session, key=456, lazy_load=True)

        c.tasks = [Task(self.session, key=3, lazy_load=True), Task(self.session, key=4, lazy_load=True), Task(self.session, key=2, lazy_load=True)]
        c.opportunities = [Opportunity(self.session, key=45, lazy_load=True), Opportunity(self.session, key=101, lazy_load=True), Opportunity(self.session, key=33, lazy_load=True)]
        c.cases = [Case(self.session, key=55, lazy_load=True), Case(self.session, key=89, lazy_load=True)]

        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)

        args = mockRequestsPUT.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Contact.ENDPOINT + '/445')
        self.assertEqual(data, self.contact2)
