
from endpoint import Endpoint, make_plain_property


class Contact(Endpoint):

	ENDPOINT = '/contact'

	first_name = make_plain_property('fn', basestring, '', 'Contact\'s first name')
	last_name = make_plain_property('ln', basestring, '', 'Contact\'s last name')


