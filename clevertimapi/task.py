from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_ref_property, make_single_elem_ref_property


class Task(Endpoint):

    ENDPOINT = '/task'

    name = make_single_elem_property('name', string_types, '', 'Task headline description')

    location = make_single_elem_property('location', string_types, '', 'The location where this task is suppose to take place')

    created_by = make_single_elem_ref_property('userId', 'User', 'The user who created this comment', readonly=True)
    assigned_to = make_single_elem_ref_property('aUserId', 'User', 'The user who this task is assigned to')

    case = make_multi_elem_ref_property('case', 'Case', 'A reference to a case that this task is for')
    opportunity = make_multi_elem_ref_property('opp', 'Opportunity', 'A reference to an opportunity that this task is for')

    comments = make_multi_elem_ref_property('comments', 'Comment', 'List of comments for this task')

    is_completed = make_single_elem_property('is_completed', bool, '', 'An indicator (True or False) if the task has been completed')
    is_deleted = make_single_elem_property('is_deleted', bool, '', 'An indicator (True or False) if the task has been deleted')

    # TODO: cust, atype, atypet, startDate, endDate, (rec, recevery, recurring_opts), gid


Session.register_endpoint(Task)
