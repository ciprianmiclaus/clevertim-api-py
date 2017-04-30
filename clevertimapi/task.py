from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property


class Task(Endpoint):

	ENDPOINT = '/task'

	name = make_single_elem_property('name', string_types, '', 'Task headline description')


Session.register_endpoint(Task)