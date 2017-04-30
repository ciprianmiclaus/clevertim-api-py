import base64
import logging
import json
import requests


log = logging.getLogger(__name__)


class SessionError(Exception):
	"""Raised when a REST call gets a non-2XX HTTP error code."""


class Session(object):

	ENDPOINT_URL = 'https://www.clevertim.com/api'
	
	ENDPOINT_FACTORY = {}

	def __init__(self, api_key, endpoint_url=None, enable_caching=True):
		assert api_key, "Empty API key"
		self.api_key = api_key
		endpoint_url = endpoint_url or self.ENDPOINT_URL
		self.endpoint_url = endpoint_url.rstrip('/')
		self.enable_caching = enable_caching
		# used to cache GET requests
		self.session_cache = {}
		self.instance_cache = {}

	@classmethod
	def register_endpoint(cls, endpoint_cls):
		cls.ENDPOINT_FACTORY[endpoint_cls.__name__] = endpoint_cls

	@classmethod
	def deregister_endpoint(cls, endpoint_cls):
		del cls.ENDPOINT_FACTORY[endpoint_cls.__name__]

	@classmethod
	def enpoint_name_to_cls(cls, endpoint_name):
		return cls.ENDPOINT_FACTORY[endpoint_name]
		
	def _get_url(self, endpoint, resource_id=None):
		url = self.endpoint_url
		if not endpoint.startswith('/'):
			url += '/'
		url += endpoint.rstrip('/')
		if resource_id:
			url += '/' + str(resource_id)
		return url

	def _get_cache_key(self, endpoint, resource_id):
		return '%s%s' % (endpoint, resource_id)

	def _get_cached_value(self, endpoint, resource_id):
		if self.enable_caching:
			cache_key = self._get_cache_key(endpoint, resource_id)
			ret = self.session_cache.get(cache_key)
			if ret:
				return ret

	def _update_cache(self, endpoint, resource_id, result):
		if self.enable_caching:
			for res in result:
				cache_key = self._get_cache_key(endpoint, res['id'])
				self.session_cache[cache_key] = res

	def make_request(self, endpoint, resource_id=None, method='GET', payload=None, reload=False):
		assert endpoint, "Empty endpoint"

		auth_key = self.api_key + ':X'
		auth_token = base64.standard_b64encode(auth_key.encode('ascii'))
		headers = {
			'Authorization': 'Basic %s' % (auth_token,),
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}

		url = self._get_url(endpoint, resource_id=resource_id)

		cache_key = None
		if method == "GET":
			if not reload:
				val = self._get_cached_value(endpoint, resource_id)
				if val is not None:
					log.debug("cache hit on GET %s", url)
					return val
			log.debug("GET %s", url)
			r = requests.get(url, headers = headers)
		elif method == "POST":
			log.debug("POST %s %s", url, payload)
			#todo: post needs to update the cache
			r = requests.post(url, headers = headers, data = json.dumps(payload, separators=(',', ':')))
		elif method == "PUT":
			log.debug("PUT %s %s", url, payload)
			#todo: put needs to update the cache
			r = requests.put(url, headers = headers, data = json.dumps(payload, separators=(',', ':')))
		elif method == "DELETE":
			log.debug("DELETE %s", url)
			#todo: delete clears the cache
			r = requests.delete(url, headers = headers)
		else:
			assert False, "Unknown method: '%s'" % (method,)

		status_code = r.status_code
		response = r.text

		if status_code != 200:
			raise SessionError("HTTP %s - %s" % (status_code, response))

		log.debug("Response %s %s", r.status_code, response)
		result = response and json.loads(response) or None

		if result is not None:
			result = result['content']

			# update the cache
			if method != 'DELETE':
				self._update_cache(endpoint, resource_id, result)

			if method != 'GET' or resource_id is not None:
				result = result[0]

		return result
		
	def get(self, endpoint_name, key, lazy_load=False):
		cache_key = '%s%s' % (endpoint_name, key)
		instance = self.instance_cache.get(cache_key)
		if instance is None:
			cls = self.ENDPOINT_FACTORY[endpoint_name]
			instance = cls(self, key=key, lazy_load=lazy_load)
			self.instance_cache[cache_key] = instance
		return instance

	def get_all(self, endpoint_name):
		pass

