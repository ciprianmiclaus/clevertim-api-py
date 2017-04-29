
from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property
from session import Session


class Company(Endpoint):

	ENDPOINT = '/company'

	DEFAULTS = {
		'is_company': True
	}

	name = make_single_elem_property('cn', basestring, '', 'Company\'s name')

	address = make_single_elem_property('address', basestring, '', 'Company\'s address')
	city = make_single_elem_property('city', basestring, '', 'Company\'s city')
	postcode = make_single_elem_property('postcode', basestring, '', 'Company\'s postcode')
	region = make_single_elem_property('region', basestring, '', 'Contact\'s region/district/state code')
	country = make_single_elem_property('country', basestring, '', 'Contact\'s country code')

	description = make_single_elem_property('description', basestring, '', 'Some text about this company')

	emails = make_multi_elem_property('email', basestring, 'Company\'s list of email addresses')
	websites = make_multi_elem_property('website', basestring, 'Company\'s list of web sites')

	tags = make_multi_elem_property('tags', basestring, 'List of tags this company was tagged with.')

	tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this company')
	opportunities = make_multi_elem_ref_property('opportunities', 'Opportunity', 'List of opportunities for this company')
	cases = make_multi_elem_ref_property('cases', 'Case', 'List of cases for this company')

	notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this company')


Session.register_endpoint(Company)
