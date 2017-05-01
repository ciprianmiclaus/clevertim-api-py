from clevertimapi.endpoint import Endpoint
from clevertimapi.session import Session
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


class TestEndpoint(unittest.TestCase):

    def setUp(self):
        self.session = Session('API_KEY')

        self.payload = {
            'status': 'OK',
            'content': [{
                'id': 6789,
                'is_private': True,
                'ao': 'now',
                'lm': '2017-01-04T10:23:22Z',
                'lc': '2017-01-02T05:22:12Z',
            }]
        }

        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.payload, separators=(',', ':'))

        # just so we can test with this class
        Endpoint.ENDPOINT = '/fake'

        self.mockRequestsGET = mock.patch('requests.get', return_value=response).start()

    def tearDown(self):
        mock.patch.stopall()

    def test_lazy_load_loads_on_first_property(self):
        endpoint = Endpoint(self.session, key=1234, lazy_load=True)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(endpoint.last_contacted, '2017-01-02T05:22:12Z')
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_unlazy_load_loads_in_init(self):
        endpoint = Endpoint(self.session, key=1234, lazy_load=False)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(endpoint.last_contacted, '2017-01-02T05:22:12Z')
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_lazy_load_reload(self):
        endpoint = Endpoint(self.session, key=1234, lazy_load=True)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(self.mockRequestsGET.call_count, 0)
        endpoint.reload()
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(endpoint.last_contacted, '2017-01-02T05:22:12Z')
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    def test_unlazy_load_reload(self):
        endpoint = Endpoint(self.session, key=1234, lazy_load=False)
        self.assertFalse(endpoint.is_new())
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        self.assertEqual(endpoint.key, 1234)
        self.assertEqual(self.mockRequestsGET.call_count, 1)
        endpoint.reload()
        self.assertEqual(self.mockRequestsGET.call_count, 2)
        self.assertEqual(endpoint.visibility, Endpoint.VISIBILITY.PRIVATE)
        self.assertEqual(self.mockRequestsGET.call_count, 2)
        self.assertEqual(endpoint.added_on, 'now')
        self.assertEqual(endpoint.last_modified, '2017-01-04T10:23:22Z')
        self.assertEqual(endpoint.last_contacted, '2017-01-02T05:22:12Z')
        self.assertEqual(self.mockRequestsGET.call_count, 2)

    def test_reload_on_new_lazy_endpoint_fails(self):
        endpoint = Endpoint(self.session, lazy_load=True)
        with self.assertRaises(AssertionError):
            endpoint.reload()

    def test_reload_on_new_unlazy_endpoint_fails(self):
        endpoint = Endpoint(self.session, lazy_load=False)
        with self.assertRaises(AssertionError):
            endpoint.reload()

    def test_new_endpoints_do_not_call_get_on_properties(self):
        properties = [prop for prop in dir(Endpoint) if isinstance(getattr(Endpoint, prop), property)]
        for prop in properties:
            endpoint = Endpoint(self.session, lazy_load=True)
            getattr(endpoint, prop)
            endpoint2 = Endpoint(self.session, lazy_load=False)
            getattr(endpoint2, prop)
            self.assertEqual(self.mockRequestsGET.call_count, 0)

    def test_lazy_instance_loads_on_any_first_property_except_key(self):
        properties = [prop for prop in dir(Endpoint) if isinstance(getattr(Endpoint, prop), property)]
        cumulative_get_calls = 0
        key = 123
        for prop in properties:
            endpoint = Endpoint(self.session, key=key, lazy_load=True)
            self.assertEqual(self.mockRequestsGET.call_count, cumulative_get_calls)
            getattr(endpoint, prop)
            if prop == 'key':
                self.assertEqual(self.mockRequestsGET.call_count, cumulative_get_calls)
            else:
                cumulative_get_calls += 1
                self.assertEqual(self.mockRequestsGET.call_count, cumulative_get_calls)
            key += 1

    @mock.patch('requests.put')
    def test_save_existing_endpoint(self, mockRequestsPUT):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.payload)
        mockRequestsPUT.return_value = response

        endpoint = Endpoint(self.session, key=6789, lazy_load=False)
        endpoint.save()

        self.assertEqual(mockRequestsPUT.call_count, 1)
        session_url = mockRequestsPUT.call_args_list[0][0][0]
        data = mockRequestsPUT.call_args_list[0][1]['data']
        self.assertEqual(session_url, Session.ENDPOINT_URL + Endpoint.ENDPOINT + '/6789')
        self.assertEqual(json.loads(data), self.payload['content'][0])

    @mock.patch('requests.post')
    def test_save_new_endpoint(self, mockRequestsPOST):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.payload)
        mockRequestsPOST.return_value = response

        endpoint = Endpoint(self.session)
        self.assertTrue(endpoint.is_new())
        endpoint.save()

        self.assertEqual(mockRequestsPOST.call_count, 1)
        session_url = mockRequestsPOST.call_args_list[0][0][0]
        data = mockRequestsPOST.call_args_list[0][1]['data']
        self.assertEqual(session_url, Session.ENDPOINT_URL + Endpoint.ENDPOINT)
        self.assertEqual(json.loads(data), {})

        self.assertFalse(endpoint.is_new())
        self.assertEqual(endpoint.key, 6789)

    @mock.patch('requests.delete')
    def test_delete_unlazy_loaded_endpoint(self, mockRequestsDELETE):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.payload)
        mockRequestsDELETE.return_value = response

        endpoint = Endpoint(self.session, key=6789, lazy_load=False)
        endpoint.delete()

        mockRequestsDELETE.assert_called_once_with(Session.ENDPOINT_URL + Endpoint.ENDPOINT + '/6789', headers=mock.ANY)
        self.assertEqual(self.mockRequestsGET.call_count, 1)

    @mock.patch('requests.delete')
    def test_delete_lazy_loaded_endpoint(self, mockRequestsDELETE):
        response = mock.Mock()
        response.status_code = 200
        response.text = json.dumps(self.payload)
        mockRequestsDELETE.return_value = response

        endpoint = Endpoint(self.session, key=6789, lazy_load=True)
        endpoint.delete()

        mockRequestsDELETE.assert_called_once_with(Session.ENDPOINT_URL + Endpoint.ENDPOINT + '/6789', headers=mock.ANY)
        self.assertEqual(self.mockRequestsGET.call_count, 0)
