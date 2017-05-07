from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_single_elem_ref_property, make_multi_elem_ref_property


class Note(Endpoint):

    ENDPOINT = '/note'

    description = make_single_elem_property('desc', string_types, '', 'The text of the note')

    case = make_multi_elem_ref_property('case', 'Case', 'The case this note is filed under, if any.')
    opportunity = make_multi_elem_ref_property('opportunity', 'Opportunity', 'The opportunity this note is filed under, if any.')

    files = make_multi_elem_ref_property('files', 'File', 'List of files for this note')
    linked_files = make_multi_elem_ref_property('lfiles', 'LinkedFile', 'List of linked files for this note')

    created_by = make_single_elem_ref_property('userId', 'User', 'The user who created this note', readonly=True)

    comments = make_multi_elem_ref_property('comments', 'Comment', 'List of comments for this note')

    # TODO: type, fmt, cust, delvry, headline, emailInfo


Session.register_endpoint(Note)
