from .compat import string_types
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_single_elem_ref_property, make_multi_elem_ref_property, ValueSerializer, ValidationError
from .session import Session


class PhoneNumber(ValueSerializer):

    def __init__(self):
        self._content = {}

    @staticmethod
    def is_valid_phone_type(value):
        valid_values = ('Work', 'Home', 'Mobile', 'Fax', 'Pager')
        if value not in valid_values:
            raise ValidationError("Invalid phone type '%s'. Expected one of: %s" % (value, ', '.join(valid_values)))

    phone_number = make_single_elem_property('no', string_types, '', 'Phone number')
    phone_type = make_single_elem_property('type', string_types, '', 'Phone type: Work, Home, Mobile, Fax or Pager', validate_func=is_valid_phone_type)

    def serialize(self, value):
        no = self._content.get('no')
        if not no or not isinstance(no, string_types):
            raise ValidationError("Invalid phone number.")
        phone_type = self._content.get('type')
        self.is_valid_phone_type(phone_type)
        return self._content


class Contact(Endpoint):

    ENDPOINT = '/contact'

    DEFAULTS = {
        'is_company': False
    }

    first_name = make_single_elem_property('fn', string_types, '', 'Contact\'s first name')
    last_name = make_single_elem_property('ln', string_types, '', 'Contact\'s last name')
    title = make_single_elem_property('title', string_types, '', 'Contact\'s title')

    company = make_single_elem_ref_property('companyId', 'Company', 'Contact\'s company')

    address = make_single_elem_property('address', string_types, '', 'Contact\'s address')
    city = make_single_elem_property('city', string_types, '', 'Contact\'s city')
    postcode = make_single_elem_property('postcode', string_types, '', 'Contact\'s postcode')
    region = make_single_elem_property('region', string_types, '', 'Contact\'s region/district/state code')
    country = make_single_elem_property('country', string_types, '', 'Contact\'s country code')

    description = make_single_elem_property('description', string_types, '', 'Some text about this contact')

    emails = make_multi_elem_property('email', string_types, 'Contact\'s list of email addresses')
    websites = make_multi_elem_property('website', string_types, 'Contact\'s list of web sites')

    tags = make_multi_elem_property('tags', string_types, 'List of tags this contact was tagged with.')

    tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this contact')
    opportunities = make_multi_elem_ref_property('opportunities', 'Opportunity', 'List of opportunities for this contact')
    cases = make_multi_elem_ref_property('cases', 'Case', 'List of cases for this contact')

    notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this contact')

    @property
    def last_contacted(self):
        self._check_needs_loading()
        return self._content.get('lc')

    # TODO:
    # phones, smids, files, lfiles, gid, cphoto, cf


Session.register_endpoint(Contact)
