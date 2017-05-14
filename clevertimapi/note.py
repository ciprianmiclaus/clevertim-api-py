from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_single_elem_ref_property, make_multi_elem_ref_property, ValidationError


class Note(Endpoint):

    ENDPOINT = '/note'

    class NOTE_TYPES(object):
        PLAIN_NOTE = 'N'
        DROPBOX_EMAIL = 'E'
        EMAIL_NOTE = 'S'
        SMS_NOTE = 'M'

        ALL_VALID_VALUES = frozenset((PLAIN_NOTE, DROPBOX_EMAIL, EMAIL_NOTE, SMS_NOTE))
        ALL_VALID_SET_VALUES = frozenset((PLAIN_NOTE, EMAIL_NOTE, SMS_NOTE))

        @classmethod
        def is_valid_note_type(cls, value):
            if value not in cls.ALL_VALID_VALUES:
                raise ValidationError("Invalid note type '%s'. Expected one of: %s" % (value, ', '.join(cls.ALL_VALID_VALUES)))
            return True

        @classmethod
        def is_valid_set_note_type(cls, value):
            if value not in cls.ALL_VALID_SET_VALUES:
                raise ValidationError("Invalid note type '%s'. Expected one of: %s" % (value, ', '.join(cls.ALL_VALID_SET_VALUES)))
            return True

    class NOTE_DELIVERY_TYPES(object):
        NO_EXTERNAL_DELIVERY = 'N'
        SMS_DELIVERY_FAILED = 'F'
        SMS_DELIVERY_SUCCEEDED = 'S'

    description = make_single_elem_property('desc', string_types, '', 'The text of the note')
    note_type = make_single_elem_property('type', string_types, NOTE_TYPES.PLAIN_NOTE, 'The type of note', validate_func=NOTE_TYPES.is_valid_set_note_type)

    who = make_single_elem_ref_property('cust', 'ContactOrCompany', 'The contact or company this task is for')
    case = make_multi_elem_ref_property('case', 'Case', 'The case this note is filed under, if any.')
    opportunity = make_multi_elem_ref_property('opportunity', 'Opportunity', 'The opportunity this note is filed under, if any.')

    files = make_multi_elem_ref_property('files', 'File', 'List of files for this note')
    linked_files = make_multi_elem_ref_property('lfiles', 'LinkedFile', 'List of linked files for this note')

    created_by = make_single_elem_ref_property('userId', 'User', 'The user who created this note', readonly=True)

    comments = make_multi_elem_ref_property('comments', 'Comment', 'List of comments for this note')

    @property
    def sms_delivery_info(self):
        return self._content('delvry', Note.NOTE_DELIVERY_TYPES.NO_EXTERNAL_DELIVERY)

    # TODO: fmt, headline, emailInfo


Session.register_endpoint(Note)
