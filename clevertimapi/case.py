from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property, make_single_elem_ref_property


class Case(Endpoint):

    ENDPOINT = '/case'

    name = make_single_elem_property('name', string_types, '', 'Case headline description')
    description = make_single_elem_property('description', string_types, '', 'Some text about this case')
    lead_user = make_single_elem_ref_property('leadUser', 'User', 'The user this case is assigned to')

    tags = make_multi_elem_property('tags', string_types, 'List of tags this case was tagged with.')

    tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this case')
    notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this case')


Session.register_endpoint(Case)
