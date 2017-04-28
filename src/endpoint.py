from session import Session

def _attr_get(attr_name, default=None):
	def _get(self):
		self._check_needs_loading()
		return self._content.get(attr_name, default)
	return _get

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

	
def _single_ref_attr_get(attr_name, elem_ref_type):
	def _get(self):
		self._check_needs_loading()
		key = self._content.get(attr_name)
		if key:
			return self.session.get(elem_ref_type, key, lazy_load=True)
	return _get

def _single_ref_attr_set(attr_name, elem_ref_type):
	def _set(self, value):
		if value is not None:
			assert isinstance(value, Session.enpoint_name_to_cls(elem_ref_type))
			value = value.key
		self._content[attr_name] = value
	return _set

def make_single_elem_ref_property(attr_name, elem_ref_type, doc_string=''):
	return property(_single_ref_attr_get(attr_name, elem_ref_type), _single_ref_attr_set(attr_name, elem_ref_type), _attr_del(attr_name), doc_string)


def _multi_ref_attr_get(attr_name, elem_ref_type):
	def _get(self):
		self._check_needs_loading()
		keys = self._content.get(attr_name, [])
		return [self.session.get(elem_ref_type, key, lazy_load=True) for key in keys]
	return _get

def _multi_ref_attr_set(attr_name, elem_ref_type):
	def _set(self, value):
		if value is not None:
			assert isinstance(value, list)
			elem_ref_type_cls = Session.enpoint_name_to_cls(elem_ref_type)
			assert all(isinstance(v, elem_ref_type_cls) for v in value)
			value = [v.key for v in value]
		self._content[attr_name] = value
	return _set

def make_multi_elem_ref_property(attr_name, elem_ref_type, doc_string=''):
	return property(_multi_ref_attr_get(attr_name, elem_ref_type), _multi_ref_attr_set(attr_name, elem_ref_type), _attr_del(attr_name), doc_string)
	

class Endpoint(object):

	def __init__(self, session, key=None, lazy_load=False):
		self.session = session
		self._key = key
		self._loaded = False
		if self.key and not lazy_load:
			self._load()
		else:
			self._content = {}

	def _check_needs_loading(self):
		if self._key and not self._loaded:
			self._load()

	def _load(self, reload=False):
		assert self._key, "Cannot load a resource without a key"
		ret = self.session.make_request(self.ENDPOINT, resource_id=self._key, reload=reload)
		self._content = ret['content'][0]
		self._loaded = True

	def reload(self):
		self._load(reload=True)

	def save(self):
		method = 'PUT' if self._key else 'POST'
		ret = self.session.make_request(self.ENDPOINT, resource_id=self.key, method=method, payload=self._content)
		self._content = ret['content'][0]
		self._key = self._content['id']
		self._loaded = True

	def delete(self):
		self.session.make_request(self.ENDPOINT, resource_id=self._key, method='DELETE')
		self._key = None

	def is_new(self):
		return not self._key

	@property
	def key(self):
		return self._key

	@property
	def is_private(self):
		self._check_needs_loading()
		return self._content.get('is_private', False)

	@property
	def added_on(self):
		self._check_needs_loading()
		return self._content.get('ao')

	@property
	def last_modified(self):
		self._check_needs_loading()
		return self._content.get('lm')

	@property
	def last_contacted(self):
		self._check_needs_loading()
		return self._content.get('lc')


