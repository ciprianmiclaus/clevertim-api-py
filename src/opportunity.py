from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property
from session import Session


class Opportunity(Endpoint):

	ENDPOINT = '/opportunity'

	name = make_single_elem_property('name', basestring, '', 'Opportunity headline description')

	tags = make_multi_elem_property('tags', basestring, 'List of tags this opportunity was tagged with.')

	tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this oppotunity')

	notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this opportunity')


Session.register_endpoint(Opportunity)