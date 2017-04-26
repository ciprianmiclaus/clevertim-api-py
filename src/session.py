import base64
import logging
import json
import requests


log = logging.getLogger(__name__)


class SessionError(Exception):
	"""Raised when a REST call gets a non-2XX HTTP error code."""


class Session(object):

	ENDPOINT_URL = 'https://www.clevertim.com/api'

	def __init__(self, api_key, endpoint_url=None):
		assert api_key, "Empty API key"
		self.api_key = api_key
		endpoint_url = endpoint_url or self.ENDPOINT_URL
		self.endpoint_url = endpoint_url.rstrip('/')

	def _get_url(self, endpoint, resource_id=None):
		url = self.endpoint_url
		if not endpoint.startswith('/'):
			url += '/'
		url += endpoint.rstrip('/')
		if resource_id:
			url += '/' + str(resource_id)
		return url

	def make_request(self, endpoint, resource_id=None, method='GET', payload=None):
		assert endpoint, "Empty endpoint"

		auth_token = base64.standard_b64encode(self.api_key + ':X')
		headers = {
			'Authorization': 'Basic %s' % (auth_token,),
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}

		url = self._get_url(endpoint, resource_id=resource_id)

		if method == "GET":
			log.debug("GET %s", url)
			r = requests.get(url, headers = headers)
		elif method == "POST":
			log.debug("POST %s %s", url, payload)
			r = requests.post(url, headers = headers, data = payload)
		elif method == "PUT":
			log.debug("PUT %s %s", url, payload)
			r = requests.put(url, headers = headers, data = payload)
		elif method == "DELETE":
			log.debug("DELETE %s", url)
			r = requests.delete(url, headers = headers)
		else:
			assert False, "Unknown method: '%s'" % (method,)

		status_code = r.status_code
		response = r.text

		if status_code != 200:
			raise SessionError("HTTP %s - %s" % (status_code, response))

		log.debug("Response %s %s", r.status_code, response)
		if response:
			return json.loads(response)
