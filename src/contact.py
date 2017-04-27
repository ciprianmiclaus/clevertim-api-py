
from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property


"""
Ref properties requirements:
	X. has a key (id) property
	X. has an actual object property - loaded lazily
	X. if either one gets set, the other one is updated automatically
	X. save works
	X. supports single property or list of references

"""

class Contact(Endpoint):

	ENDPOINT = '/contact'

	first_name = make_single_elem_property('fn', basestring, '', 'Contact\'s first name')
	last_name = make_single_elem_property('ln', basestring, '', 'Contact\'s last name')
	title = make_single_elem_property('title', basestring, '', 'Contact\'s title')

	company_key = make_single_elem_property('companyId', int, None, 'Contact\'s company key')
	company = make_single_elem_ref_property('companyId', int, )

	address = make_single_elem_property('title', basestring, '', 'Contact\'s address')
	city = make_single_elem_property('city', basestring, '', 'Contact\'s city')
	postcode = make_single_elem_property('postcode', basestring, '', 'Contact\'s postcode')

	description = make_single_elem_property('description', basestring, '', 'Some text about this contact')

	emails = make_multi_elem_property('email', basestring, 'Contact\'s list of email addresses')
	websites = make_multi_elem_property('website', basestring, 'Contact\'s list of web sites')

	tags = make_multi_elem_property('tags', basestring, 'List of tags this contact was tagged with.')
