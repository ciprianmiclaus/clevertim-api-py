from .compat import string_types
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_single_elem_ref_property, make_multi_elem_ref_property
from .session import Session


class Contact(Endpoint):

	ENDPOINT = '/contact'

	DEFAULTS = {
		'is_company': False
	}

	first_name = make_single_elem_property('fn', string_types, '', 'Contact\'s first name')
	last_name = make_single_elem_property('ln', string_types, '', 'Contact\'s last name')
	title = make_single_elem_property('title', string_types, '', 'Contact\'s title')

	company = make_single_elem_ref_property('companyId', 'Company', 'Contact\'s company')

	address = make_single_elem_property('address', string_types, '', 'Contact\'s address')
	city = make_single_elem_property('city', string_types, '', 'Contact\'s city')
	postcode = make_single_elem_property('postcode', string_types, '', 'Contact\'s postcode')
	region = make_single_elem_property('region', string_types, '', 'Contact\'s region/district/state code')
	country = make_single_elem_property('country', string_types, '', 'Contact\'s country code')

	description = make_single_elem_property('description', string_types, '', 'Some text about this contact')

	emails = make_multi_elem_property('email', string_types, 'Contact\'s list of email addresses')
	websites = make_multi_elem_property('website', string_types, 'Contact\'s list of web sites')

	tags = make_multi_elem_property('tags', string_types, 'List of tags this contact was tagged with.')

	tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this contact')
	opportunities = make_multi_elem_ref_property('opportunities', 'Opportunity', 'List of opportunities for this contact')
	cases = make_multi_elem_ref_property('cases', 'Case', 'List of cases for this contact')

	notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this contact')

	#TODO:
	# phones, smids, files, lfiles, gid, cphoto, cf


Session.register_endpoint(Contact)



