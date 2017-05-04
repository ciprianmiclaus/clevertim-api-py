from clevertimapi.session import Session
from clevertimapi.company import Company, PhoneNumber, SocialMediaId
from clevertimapi.task import Task
from clevertimapi.opportunity import Opportunity
from clevertimapi.case import Case
from copy import deepcopy
from mock_utils import setup_requests_call_mock
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


class TestCompany(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')

        self.company1 = {
            'cn': 'Clevertim Ltd.',
            'is_company': True,
            'address': '199 Maverick Road',
            'city': 'London',
            'postcode': 'SW19 7BH',
            'region': 'US-FL',
            'country': 'US',
            'description': 'Clevertim is a great company. They do software.',
            'email': ['sales@gmail.com', 'support@yahoo.com'],
            'website': ['http://www.clevertim.com', 'http://www.clevertim.org'],
            'phones': [{'no': '07979463643', 'type': 'Work'}, {'no': '07979363643', 'type': 'Home'}, {'no': '07979163643', 'type': 'Mobile'}],
            'smids': [{'smid': 'mikesp40', 'type': 'Google+'}, {'smid': 'ciprianmiclaus', 'type': 'Github'}, {'smid': 'cippy', 'type': 'Skype'}],
            'tags': ['tag1', 'tag2', 'tag3'],
            'tasks': [1, 2],
            'opportunities': [100, 101, 211],
            'cases': [55, 57],
        }
        self.company1_ret = deepcopy(self.company1)
        self.company1_ret.update({
            'id': 445,
            'lc': '2017-01-02T05:22:12Z',
        })
        self.company2 = {
            'id': 445,
            'cn': 'Some Ltd.',
            'is_company': True,
            'address': '32 Bossy Lane',
            'city': 'Winchester',
            'postcode': 'WH7 8AB',
            'region': 'GB-WRL',
            'country': 'GB',
            'description': 'Some Ltd. is fantastic. Its customer support is unlike anything out there.',
            'email': ['support@someltd.com', 'some.ltd@yahoo.com'],
            'website': ['http://www.johnrowdy.com', 'http://www.yahoo.com'],
            'phones': [{'no': '+4407979463643', 'type': 'Fax'}, {'no': '+4407979363643', 'type': 'Pager'}, {'no': '+4407979163643', 'type': 'Work'}],
            'smids': [{'smid': 'dumbo33', 'type': 'YouTube'}, {'smid': 'miky22', 'type': 'Whatsapp'}],
            'tags': ['othertag1', 'othertag2', 'othertag3'],
            'tasks': [3, 4, 2],
            'opportunities': [45, 101, 33],
            'cases': [55, 89],
            'lc': '2017-01-02T05:22:12Z',
        }

    def _compare_against_company1_ret(self, c):
        self.assertEqual(c.key, 445)
        self.assertEqual(c.name, 'Clevertim Ltd.')
        self.assertEqual(c.address, '199 Maverick Road')
        self.assertEqual(c.city, 'London')
        self.assertEqual(c.postcode, 'SW19 7BH')
        self.assertEqual(c.region, 'US-FL')
        self.assertEqual(c.country, 'US')
        self.assertEqual(c.description, 'Clevertim is a great company. They do software.',)
        self.assertEqual(c.emails, ['sales@gmail.com', 'support@yahoo.com'])
        self.assertEqual(c.websites, ['http://www.clevertim.com', 'http://www.clevertim.org'])
        self.assertEqual(c.phone_numbers, [
            PhoneNumber(phone_number='07979463643', phone_type='Work'),
            PhoneNumber(phone_number='07979363643', phone_type='Home'),
            PhoneNumber(phone_number='07979163643', phone_type='Mobile'),
        ])
        self.assertEqual(c.social_media_ids, [
            SocialMediaId(social_media_id='mikesp40', social_media_type='Google+'),
            SocialMediaId(social_media_id='ciprianmiclaus', social_media_type='Github'),
            SocialMediaId(social_media_id='cippy', social_media_type='Skype'),
        ])
        self.assertEqual(c.tags, ['tag1', 'tag2', 'tag3'])

        self.assertTrue(all(isinstance(t, Task) for t in c.tasks))
        self.assertEqual([t.key for t in c.tasks], [1, 2])
        self.assertTrue(all(isinstance(t, Opportunity) for t in c.opportunities))
        self.assertEqual([t.key for t in c.opportunities], [100, 101, 211])
        self.assertTrue(all(isinstance(t, Case) for t in c.cases))
        self.assertEqual([t.key for t in c.cases], [55, 57])

        self.assertEqual(c.last_contacted, '2017-01-02T05:22:12Z')

    @mock.patch('requests.get')
    def test_load_company(self, mockRequestsGET):
        setup_requests_call_mock(mockRequestsGET, {
            '/company/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.company1_ret
                    ]
                })
            )
        })

        c = Company(self.session, key=445)
        self.assertFalse(c.is_new())
        self._compare_against_company1_ret(c)

    @mock.patch('requests.post')
    def test_add_new_company(self, mockRequestsPOST):
        setup_requests_call_mock(mockRequestsPOST, {
            '/company': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.company1_ret
                    ]
                })
            )
        })

        c = Company(self.session)
        c.name = 'Clevertim Ltd.'
        c.address = '199 Maverick Road'
        c.city = 'London'
        c.postcode = 'SW19 7BH'
        c.region = 'US-FL'
        c.country = 'US'
        c.description = 'Clevertim is a great company. They do software.'
        c.emails = ['sales@gmail.com', 'support@yahoo.com']
        c.websites = ['http://www.clevertim.com', 'http://www.clevertim.org']
        c.phone_numbers = [
            PhoneNumber(phone_number='07979463643', phone_type='Work'),
            PhoneNumber(phone_number='07979363643', phone_type='Home'),
            PhoneNumber(phone_number='07979163643', phone_type='Mobile'),
        ]
        c.social_media_ids = [
            SocialMediaId(social_media_id='mikesp40', social_media_type='Google+'),
            SocialMediaId(social_media_id='ciprianmiclaus', social_media_type='Github'),
            SocialMediaId(social_media_id='cippy', social_media_type='Skype'),
        ]
        c.tags = ['tag1', 'tag2', 'tag3']

        c.tasks = [Task(self.session, key=1, lazy_load=True), Task(self.session, key=2, lazy_load=True)]
        c.opportunities = [Opportunity(self.session, key=100, lazy_load=True), Opportunity(self.session, key=101, lazy_load=True), Opportunity(self.session, key=211, lazy_load=True)]
        c.cases = [Case(self.session, key=55, lazy_load=True), Case(self.session, key=57, lazy_load=True)]

        self.assertTrue(c.is_new())
        c.save()
        self.assertFalse(c.is_new())
        self.assertEqual(c.key, 445)

        args = mockRequestsPOST.call_args_list[0]
        session_url = args[0][0]
        data = json.loads(args[1]['data'])

        self.assertEqual(session_url, Session.ENDPOINT_URL + Company.ENDPOINT)
        self.assertEqual(data, self.company1)

        self._compare_against_company1_ret(c)

    @mock.patch('requests.put')
    @mock.patch('requests.get')
    def test_edit_existing_company(self, mockRequestsGET, mockRequestsPUT):
        setup_requests_call_mock(mockRequestsGET, {
            '/company/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.company1_ret
                    ]
                })
            )
        })
        setup_requests_call_mock(mockRequestsPUT, {
            '/company/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        {
                            'id': 445,
                            'lc': '2017-01-02T05:22:12Z',
                        }
                    ]
                })
            )
        })

        c = Company(self.session, key=445)
        c.name = 'Some Ltd.'
        c.address = '32 Bossy Lane'
        c.city = 'Winchester'
        c.postcode = 'WH7 8AB'
        c.region = 'GB-WRL'
        c.country = 'GB'
        c.description = 'Some Ltd. is fantastic. Its customer support is unlike anything out there.'
        c.emails = ['support@someltd.com', 'some.ltd@yahoo.com']
        c.websites = ['http://www.johnrowdy.com', 'http://www.yahoo.com']
        c.phone_numbers = [
            PhoneNumber(phone_number='+4407979463643', phone_type='Fax'),
            PhoneNumber(phone_number='+4407979363643', phone_type='Pager'),
            PhoneNumber(phone_number='+4407979163643', phone_type='Work'),
        ]
        c.social_media_ids = [
            SocialMediaId(social_media_id='dumbo33', social_media_type='YouTube'),
            SocialMediaId(social_media_id='miky22', social_media_type='Whatsapp'),
        ]
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

        self.assertEqual(session_url, Session.ENDPOINT_URL + Company.ENDPOINT + '/445')
        self.assertEqual(data, self.company2)
