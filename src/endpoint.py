
def _attr_get(attr_name, default=None):
	return lambda self: self._content.get(attr_name, default)

def _attr_del(attr_name):
	def _del(self):
		del self._content[attr_name]
	return _del

def _single_attr_set(attr_name, attr_type):
	def _set(self, value):
		assert isinstance(value, attr_type) or value is None
		self._content[attr_name] = value
	return _set
	
def _multi_attr_set(attr_name, list_elem_type):
	def _set(self, value):
		assert isinstance(value, list) or value is None
		assert all(isinstance(elem, list_elem_type) for elem in value)
		self._content[attr_name] = value

def make_single_elem_property(attr_name, elem_type, default=None, doc_string=''):
	return property(_attr_get(attr_name, default), _single_attr_set(attr_name, elem_type), _attr_del(attr_name), doc_string)

def make_multi_elem_property(attr_name, elem_type, doc_string=''):
	return property(_attr_get(attr_name, default=[]), _multi_attr_set(attr_name, elem_type), _attr_del(attr_name), doc_string)


class Endpoint(object):

	def __init__(self, session, key=None):
		self.session = session
		self.key = key
		if self.key:
			self._load()
		else:
			self._content = {}

	def _load(self, reload=False):
		assert self.key, "Cannot load a resource without a key"
		ret = self.session.make_request(self.ENDPOINT, resource_id=self.key, reload=reload)
		self._content = ret['content'][0]

	def reload(self):
		self._load(reload=True)

	def save(self):
		method = 'PUT' if self.key else 'POST'
		ret = self.session.make_request(self.ENDPOINT, resource_id=self.key, method=method, payload=self._content)

	def delete(self):
		self.session.make_request(self.ENDPOINT, resource_id=self.key, method='DELETE')

	@property
	def key(self):
		return self.key

	@property
	def is_private(self):
		return self._content.get('is_private', False)

	@property
	def added_on(self):
		return self._content['ao']

	@property
	def last_modified(self):
		return self._content['lm']

	@property
	def last_contacted(self):
		return self._content['lc']


