from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, ValidationError


class CustomField(Endpoint):

    ENDPOINT = '/customfield'

    class FIELD_TYPE(object):
        INPUT = 'input'
        SELECT = 'select'
        DATE = 'date'
        USER = 'user'
        COUNTRY = 'country'
        STATE = 'state'
        REGION = 'region'
        CONTACT = 'contact'
        COMPANY = 'company'
        CASE = 'case'
        OPPORTUNITY = 'opportunity'
        CURRENCY = 'currency'

        @classmethod
        def is_valid_field_type(cls, value):
            return value in (
                cls.INPUT,
                cls.SELECT,
                cls.DATE,
                cls.USER,
                cls.COUNTRY,
                cls.STATE,
                cls.REGION,
                cls.CONTACT,
                cls.COMPANY,
                cls.CASE,
                cls.OPPORTUNITY,
                cls.CURRENCY,
            )

    class FIELD_SCOPE(object):
        CONTACTS = 'customers'
        COMPANIES = 'companies'
        CASES = 'cases'
        OPPORTUNITIES = 'opportunities'

        @classmethod
        def is_valid_field_scope(cls, value):
            return value in (
                cls.CONTACTS,
                cls.COMPANIES,
                cls.CASES,
                cls.OPPORTUNITIES,
            )

    name = make_single_elem_property('name', string_types, '', 'The name of the custom field')
    full_name = make_single_elem_property('fullname', string_types, '', 'The full name of the custom field (where the custom field has an application specific prefix)')

    field_type = make_single_elem_property('elemType', string_types, '', 'The type of the custom field', validate_func=FIELD_TYPE.is_valid_field_type)
    field_scope = make_multi_elem_property('modelType', string_types, 'The scope of the custom field (what it is applicable to)', validate_func=FIELD_SCOPE.is_valid_field_scope)
    # TODO: app = ''

    is_multi_value = make_single_elem_property('multiple', bool, '', 'Specifies if this custom field allows multiple values or just a single value')

    allowed_values = make_multi_elem_property('values', string_types, 'The list of values allowed. Only populated for custom fields of type select.')

    def validate(self):
        elem_type = self._content.get('elemType')
        if elem_type == self.FIELD_TYPE.SELECT and not self.allowed_values:
            raise ValidationError("A select custom field needs to specify the allowed_values property.")


class CustomFieldValue(object):
    pass
    # custom_field
    # value


Session.register_endpoint(CustomField)
