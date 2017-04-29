from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property
from session import Session


class Opportunity(Endpoint):

	ENDPOINT = '/opportunity'

	name = make_single_elem_property('name', basestring, '', 'Opportunity headline text')
	description = make_single_elem_property('description', basestring, '', 'Some text about this opportunity')
	lead_user = make_single_elem_ref_property('leadUser', 'User', 'The user this opportunity is assigned to')
	
	currency = make_single_elem_property('currency', basestring, '', 'The currency code (e.g. USD, EUR, GBP)')
	value = make_single_elem_property('value', basestring, '', 'The value of this deal')
	status = make_single_elem_property('status', basestring, '', 'The pipeline state of this opportunity')

	tags = make_multi_elem_property('tags', basestring, 'List of tags this opportunity was tagged with.')

	tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this oppotunity')
	notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this opportunity')


Session.register_endpoint(Opportunity)