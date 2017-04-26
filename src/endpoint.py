class Endpoint(object):

	def __init__(self, session, key=None):
		self.session = session
		self.key = key
		if self.key:
			self._load()
		else:
			self._content = {}

	def _load(self):
		assert self.key, "Cannot load a resource without a key"
		ret = self.session.make_request(self.ENDPOINT, resource_id=self.key)
		self._content = ret['content'][0]

	def reload(self):
		self._load()

	def save(self):
		method = 'PUT' if self.key else 'POST'
		ret = self.session.make_request(self.ENDPOINT, resource_id=self.key, method=method, payload=self._content)

	def delete(self):
		self.session.make_request(self.ENDPOINT, resource_id=self.key, method='DELETE')


def _plain_attr_get(attr_name, default=None):
	return lambda self: self._content.get(attr_name, default)

def _plain_attr_set(attr_name, attr_type):
	def _set(self, value):
		assert isinstance(value, attr_type)
		self._content[attr_name] = value
	return _set

def _plain_attr_del(attr_name):
	def _del(self):
		del self._content[attr_name]
	return _del

def make_plain_property(attr_name, attr_type, default=None, doc_string=''):
	return property(_plain_attr_get(attr_name, default), _plain_attr_set(attr_name, attr_type), _plain_attr_del(attr_name), doc_string)
