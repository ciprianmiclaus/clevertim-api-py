from .compat import string_types
from .contact import PhoneNumber
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, make_multi_elem_ref_property
from .session import Session


class Company(Endpoint):

    ENDPOINT = '/company'

    DEFAULTS = {
        'is_company': True
    }

    name = make_single_elem_property('cn', string_types, '', 'Company\'s name')

    address = make_single_elem_property('address', string_types, '', 'Company\'s address')
    city = make_single_elem_property('city', string_types, '', 'Company\'s city')
    postcode = make_single_elem_property('postcode', string_types, '', 'Company\'s postcode')
    region = make_single_elem_property('region', string_types, '', 'Contact\'s region/district/state code')
    country = make_single_elem_property('country', string_types, '', 'Contact\'s country code')

    description = make_single_elem_property('description', string_types, '', 'Some text about this company')

    emails = make_multi_elem_property('email', string_types, 'Company\'s list of email addresses')
    websites = make_multi_elem_property('website', string_types, 'Company\'s list of web sites')
    phone_numbers = make_multi_elem_property('phones', PhoneNumber, 'Company\'s list of phone numbers', custom_type=PhoneNumber)

    tags = make_multi_elem_property('tags', string_types, 'List of tags this company was tagged with.')

    tasks = make_multi_elem_ref_property('tasks', 'Task', 'List of tasks for this company')
    opportunities = make_multi_elem_ref_property('opportunities', 'Opportunity', 'List of opportunities for this company')
    cases = make_multi_elem_ref_property('cases', 'Case', 'List of cases for this company')

    notes = make_multi_elem_ref_property('notes', 'Note', 'List of notes for this company')

    @property
    def last_contacted(self):
        self._check_needs_loading()
        return self._content.get('lc')


Session.register_endpoint(Company)
