import datetime
from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_ref_property, make_single_elem_ref_property, ValidationError


def date_transform_from_content(content, session):
    year = content.get('y')
    if year:
        year = int(year)
        month = content.get('mo')
        if month:
            month = int(month)
            day = content.get('d')
            if day:
                return datetime.date(year, month, day)


def date_transform_to_content(content, attr_name, value):
    if not isinstance(value, datetime.date):
        raise ValidationError("Expected datetime.date and not %s" % (type(value,)))
    content.setdefault(attr_name, {}).update({'y': value.year, 'mo': value.month, 'd': value.day})


def time_transform_from_content(content, session):
    hour = content.get('h')
    if hour is not None:
        hour = int(hour)
        minute = content.get('mi')
        if minute is not None:
            minute = int(minute)
            return datetime.time(hour=hour, minute=minute)


def time_transform_to_content(content, attr_name, value):
    if not isinstance(value, datetime.time):
        raise ValidationError("Expected datetime.time and not %s" % (type(value,)))
    content.setdefault(attr_name, {}).update({'h': value.hour, 'mi': value.minute})


class Task(Endpoint):

    ENDPOINT = '/task'

    class TASK_TYPES(object):
        APPOINTMENT = 'Appointment'
        EMAIL = 'Email'
        MEETING = 'Meeting'
        CALL = 'Call'
        FOLLOWUP = 'Follow up'
        TODO = 'TO DO'
        NOTSET = 'Not set'

        ALL_VALID_VALUES = frozenset((APPOINTMENT, EMAIL, MEETING, CALL, FOLLOWUP, TODO, NOTSET))

        @classmethod
        def is_valid_task_type(cls, value):
            if value not in cls.ALL_VALID_VALUES:
                raise ValidationError("Invalid task type '%s'. Expected one of: %s" % (value, ', '.join(cls.ALL_VALID_VALUES)))
            return True

    class TASK_RECURRING_OPTIONS(object):
        NOT_RECURRING = 'N'
        DAILY = 'D'
        WEEKLY = 'W'
        MONTHLY = 'M'
        YEARLY = 'Y'

        ALL_VALID_VALUES = frozenset((NOT_RECURRING, DAILY, WEEKLY, MONTHLY, YEARLY))

        @classmethod
        def is_valid_recurring_option(cls, value):
            if value not in cls.ALL_VALID_VALUES:
                raise ValidationError("Invalid recurring option '%s'. Expected one of: %s" % (value, ', '.join(cls.ALL_VALID_VALUES)))
            return True

    name = make_single_elem_property('name', string_types, '', 'Task headline description')
    task_type = make_single_elem_property('atype', string_types, TASK_TYPES.NOTSET, 'The type of task', validate_func=TASK_TYPES.is_valid_task_type)

    location = make_single_elem_property('location', string_types, '', 'The location where this task is suppose to take place')
    who = make_single_elem_ref_property('cust', 'ContactOrCompany', 'The contact or company this task is for')

    start_date = make_single_elem_property('startDate', datetime.date, None, 'Start date for the task', transform_func=date_transform_to_content, custom_type=date_transform_from_content)
    start_time = make_single_elem_property('startDate', datetime.time, None, 'Start time for the task', transform_func=time_transform_to_content, custom_type=time_transform_from_content)
    end_date = make_single_elem_property('endDate', datetime.date, None, 'End date for the task', transform_func=date_transform_to_content, custom_type=date_transform_from_content)
    end_time = make_single_elem_property('endDate', datetime.time, None, 'End time for the task', transform_func=time_transform_to_content, custom_type=time_transform_from_content)

    created_by = make_single_elem_ref_property('userId', 'User', 'The user who created this comment', readonly=True)
    assigned_to = make_single_elem_ref_property('aUserId', 'User', 'The user who this task is assigned to')

    case = make_multi_elem_ref_property('case', 'Case', 'A reference to a case that this task is for')
    opportunity = make_multi_elem_ref_property('opp', 'Opportunity', 'A reference to an opportunity that this task is for')

    comments = make_multi_elem_ref_property('comments', 'Comment', 'List of comments for this task')

    is_completed = make_single_elem_property('is_completed', bool, False, 'An indicator (True or False) if the task has been completed')
    is_deleted = make_single_elem_property('is_deleted', bool, False, 'An indicator (True or False) if the task has been deleted')

    recurring_option = make_single_elem_property('rec', string_types, TASK_RECURRING_OPTIONS.NOT_RECURRING, 'The recurring option for this task', validate_func=TASK_RECURRING_OPTIONS.is_valid_recurring_option)
    recurring_every = make_single_elem_property('recevery', int, 1, 'The frequency of the recurring (e.g. every 3 days)')
    # TODO: (recurring_opts)


Session.register_endpoint(Task)
