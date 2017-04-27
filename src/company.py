
from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property


class Company(Endpoint):

	ENDPOINT = '/company'

	name = make_single_elem_property('cn', basestring, '', 'Company\'s name')

	address = make_single_elem_property('title', basestring, '', 'Company\'s address')
	city = make_single_elem_property('city', basestring, '', 'Company\'s city')
	postcode = make_single_elem_property('postcode', basestring, '', 'Company\'s postcode')

	description = make_single_elem_property('description', basestring, '', 'Some text about this company')

	emails = make_multi_elem_property('email', basestring, 'Contact\'s list of email addresses')
	websites = make_multi_elem_property('website', basestring, 'Contact\'s list of web sites')

	tags = make_multi_elem_property('tags', basestring, 'List of tags this contact was tagged with.')
