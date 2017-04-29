import json
import mock
import unittest

import sys
sys.path.append('../src')

from session import Session, SessionError


class FakeEndpoint(object):
	def __init__(self, session, key=None, lazy_load=False):
		pass


class TestSession(unittest.TestCase):

	def test_get_without_register_fails(self):
		session = Session(api_key='APIKEY')
		with self.assertRaises(KeyError):
			session.get('FakeEndpoint', key=1, lazy_load=True)

	def test_enpoint_name_to_cls(self):
		Session.register_endpoint(FakeEndpoint)
		self.assertTrue(Session.enpoint_name_to_cls('FakeEndpoint') is FakeEndpoint)
		Session.deregister_endpoint(FakeEndpoint)
			
	def test_get_after_deregister_fails(self):
		session = Session(api_key='APIKEY')
		Session.register_endpoint(FakeEndpoint)
		Session.deregister_endpoint(FakeEndpoint)
		with self.assertRaises(KeyError):
			session.get('FakeEndpoint', key=1, lazy_load=True)

	def test_register_get(self):
		session = Session(api_key='APIKEY')
		Session.register_endpoint(FakeEndpoint)
		ret = session.get('FakeEndpoint', key=1, lazy_load=True)
		self.assertIsInstance(ret, FakeEndpoint)
		#seccond request hit the cache
		ret2 = session.get('FakeEndpoint', key=1, lazy_load=True)
		self.assertIsInstance(ret2, FakeEndpoint)
		self.assertTrue(ret is ret2)
		Session.deregister_endpoint(FakeEndpoint)

	def test_invalid_method_raises(self):
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake')
		with self.assertRaises(AssertionError):
			session.make_request(endpoint='/endpoint', resource_id=3434, method='INVALID')
		
	@mock.patch('requests.get')
	def test_make_request_get(self, mockRequestsGET):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 200
		response.text = json.dumps(payload)
		mockRequestsGET.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake')
		ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
		self.assertEqual(ret, payload)
		mockRequestsGET.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers = mock.ANY)

	@mock.patch('requests.get')
	def test_make_request_get_invalid_http_code_raises(self, mockRequestsGET):	
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 500
		response.text = json.dumps(payload)
		mockRequestsGET.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake')
		with self.assertRaises(SessionError):
			ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')

	@mock.patch('requests.post')
	def test_make_request_post(self, mockRequestsPOST):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 200
		response.text = json.dumps(payload)
		mockRequestsPOST.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
		ret = session.make_request(endpoint='endpoint', method='POST', payload=payload)
		self.assertEqual(ret, payload)
		mockRequestsPOST.assert_called_once_with('http://localhost:8000/fake/endpoint', headers = mock.ANY, data=json.dumps(payload, separators=(',', ':')))

	@mock.patch('requests.post')
	def test_make_request_post_invalid_http_code_raises(self, mockRequestsPOST):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 401
		response.text = json.dumps(payload)
		mockRequestsPOST.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
		with self.assertRaises(SessionError):
			ret = session.make_request(endpoint='endpoint', method='POST', payload=payload)

	@mock.patch('requests.put')
	def test_make_request_put(self, mockRequestsPUT):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 200
		response.text = json.dumps(payload)
		mockRequestsPUT.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
		ret = session.make_request(endpoint='endpoint', resource_id=3434, method='PUT', payload=payload)
		self.assertEqual(ret, payload)
		mockRequestsPUT.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers = mock.ANY, data=json.dumps(payload, separators=(',', ':')))

	@mock.patch('requests.put')
	def test_make_request_put_invalid_http_code_raises(self, mockRequestsPUT):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 404
		response.text = json.dumps(payload)
		mockRequestsPUT.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
		with self.assertRaises(SessionError):
			session.make_request(endpoint='endpoint', resource_id=3434, method='PUT', payload=payload)

	@mock.patch('requests.delete')
	def test_make_request_delete(self, mockRequestsDELETE):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 200
		response.text = json.dumps(payload)
		mockRequestsDELETE.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
		ret = session.make_request(endpoint='endpoint', resource_id='333', method='DELETE', payload=None)
		self.assertEqual(ret, payload)
		mockRequestsDELETE.assert_called_once_with('http://localhost:8000/fake/endpoint/333', headers = mock.ANY)

	@mock.patch('requests.delete')
	def test_make_request_delete_invalid_http_code_raises(self, mockRequestsDELETE):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 470
		response.text = json.dumps(payload)
		mockRequestsDELETE.return_value = response
		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake/')
		with self.assertRaises(SessionError):
			session.make_request(endpoint='endpoint', resource_id='333', method='DELETE', payload=None)

	@mock.patch('requests.get')
	def test_caching_enabled_2nd_get_hits_cache(self, mockRequestsGET):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 200
		response.text = json.dumps(payload)
		mockRequestsGET.return_value = response

		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake', enable_caching=True)
		ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
		self.assertIsNotNone(ret)
		# 2nd request should hit the cache
		ret2 = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET') 
		mockRequestsGET.assert_called_once_with('http://localhost:8000/fake/endpoint/3434', headers = mock.ANY)
		self.assertTrue(ret is ret2)

	@mock.patch('requests.get')
	def test_caching_enabled_2nd_get_with_reload_hits_server(self, mockRequestsGET):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 200
		response.text = json.dumps(payload)
		mockRequestsGET.return_value = response

		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake', enable_caching=True)
		ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
		self.assertIsNotNone(ret)
		# 2nd request should hit the cache
		ret2 = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET', reload=True) 
		self.assertEqual(mockRequestsGET.call_count, 2)
		self.assertTrue(ret is not ret2)
		self.assertEqual(ret, ret2)

	@mock.patch('requests.get')
	def test_caching_disabled_2nd_get_hits_server(self, mockRequestsGET):
		payload = { 'key1': 1, 'key2': '2', 'key3': [1, '2', [3]] }
		response = mock.Mock()
		response.status_code = 200
		response.text = json.dumps(payload)
		mockRequestsGET.return_value = response

		session = Session(api_key='APIKEY', endpoint_url='http://localhost:8000/fake', enable_caching=False)
		ret = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET')
		self.assertIsNotNone(ret)
		# 2nd request should hit the cache
		ret2 = session.make_request(endpoint='/endpoint', resource_id=3434, method='GET') 
		self.assertEqual(mockRequestsGET.call_count, 2)
		self.assertTrue(ret is not ret2)
		self.assertEqual(ret, ret2)