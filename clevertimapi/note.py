from session import Session
from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property


class Note(Endpoint):

	ENDPOINT = '/note'

	description = make_single_elem_property('desc', basestring, '', 'The text of the note')

	comments = make_multi_elem_ref_property('comments', 'Comment', 'List of comments for this note')


Session.register_endpoint(Note)