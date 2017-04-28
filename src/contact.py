
from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_single_elem_ref_property, make_multi_elem_ref_property
from session import Session


class Contact(Endpoint):

	ENDPOINT = '/contact'

	first_name = make_single_elem_property('fn', basestring, '', 'Contact\'s first name')
	last_name = make_single_elem_property('ln', basestring, '', 'Contact\'s last name')
	title = make_single_elem_property('title', basestring, '', 'Contact\'s title')

	company = make_single_elem_ref_property('companyId', 'Company', 'Contact\'s company')

	address = make_single_elem_property('address', basestring, '', 'Contact\'s address')
	city = make_single_elem_property('city', basestring, '', 'Contact\'s city')
	postcode = make_single_elem_property('postcode', basestring, '', 'Contact\'s postcode')

	description = make_single_elem_property('description', basestring, '', 'Some text about this contact')

	emails = make_multi_elem_property('email', basestring, 'Contact\'s list of email addresses')
	websites = make_multi_elem_property('website', basestring, 'Contact\'s list of web sites')

	tags = make_multi_elem_property('tags', basestring, 'List of tags this contact was tagged with.')

	tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this contact')
	opportunities = make_multi_elem_ref_property('opportunities', 'Opportunity', 'List of opportunities for this contact')
	cases = make_multi_elem_ref_property('cases', 'Case', 'List of cases for this contact')


Session.register_endpoint(Contact)



