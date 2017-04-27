from session import Session
from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property


class Case(Endpoint):

	ENDPOINT = '/case'

	name = make_single_elem_property('name', basestring, '', 'Case headline description')

	tags = make_multi_elem_property('tags', basestring, 'List of tags this case was tagged with.')

	tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this case')


Session.register_endpoint(Case)