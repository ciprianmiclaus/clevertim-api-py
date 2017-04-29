from session import Session
from endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property


class Comment(Endpoint):

	ENDPOINT = '/comment'

	description = make_single_elem_property('comment', basestring, '', 'The text of the comment')

	note = make_multi_elem_ref_property('nid', 'Note', 'The note this comment is attached to or None if not attached to a note')
	task = make_multi_elem_ref_property('tid', 'Task', 'The task this comment is attached to or None if not attached to a task')


Session.register_endpoint(Note)