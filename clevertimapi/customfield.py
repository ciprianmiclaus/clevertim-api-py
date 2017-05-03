import datetime
from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_multi_elem_property, ValidationError, ValueSerializer


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


class CustomFieldValueBase(ValueSerializer):

    def __init__(self, content=None, custom_field=None, custom_field_value=None, session=None):
        if content:
            keys = content.keys()
            assert len(keys) == 1, "Invalid CustomFieldValue content: %s" % (content,)
            key = keys[0]
            custom_field = CustomField(session, key=key, lazy_load=True)
            custom_field_value = content[key]
        self._custom_field = custom_field
        self._custom_field_value = self._validate_value(custom_field_value)

    @property
    def custom_field(self):
        return self._custom_field

    def _get_cf_value(self):
        return self._custom_field_value

    def _set_cf_value(self, value):
        self._custom_field_value = self._validate_value(value)

    custom_field_value = property(_get_cf_value, _set_cf_value, None, "The value of the custom field")

    def _get_expected_value_types(self):
        from .contact import Contact
        from .company import Company
        from .case import Case
        from .opportunity import Opportunity
        from .user import User
        return {
            CustomField.FIELD_TYPE.INPUT: string_types,
            CustomField.FIELD_TYPE.SELECT: string_types,
            CustomField.FIELD_TYPE.DATE: datetime.date,
            CustomField.FIELD_TYPE.USER: User,
            CustomField.FIELD_TYPE.COUNTRY: string_types,
            CustomField.FIELD_TYPE.STATE: string_types,
            CustomField.FIELD_TYPE.REGION: string_types,
            CustomField.FIELD_TYPE.CONTACT: Contact,
            CustomField.FIELD_TYPE.COMPANY: Company,
            CustomField.FIELD_TYPE.CASE: Case,
            CustomField.FIELD_TYPE.OPPORTUNITY: Opportunity,
            CustomField.FIELD_TYPE.CURRENCY: string_types,
        }

    def _check_expected_single_value_type(self, value):
        expected_types = self.EXPECTED_VALUE_TYPES[self._custom_field.field_type]
        if not isinstance(value, expected_types):
            raise ValidationError("Incorrect value of type '%s'. Expected type(s): '%s'" % (type(value), expected_types))

    def _check_expected_type(self, value):
        if self._custom_field.is_multi_value:
            if not isinstance(value, (list, tuple)):
                raise ValidationError("Incorrect value for a multiple values custom field. Expected a list or a tuple.")
            for val in value:
                self._check_expected_single_value_type(val)
        else:
            self._check_expected_single_value_type(value)

    def _validate_value(self, value):
        """Validates a value when set"""
        self._check_expected_type(value)
        field_type = self._custom_field.field_type
        if field_type == CustomField.FIELD_TYPE.SELECT:
            def _validate_select_value(v):
                if v not in self._custom_field.allowed_values:
                    raise ValidationError("Incorrect value '%s' for a SELECT custom field. Allowed values: %s" % (v, ', '.join(self._custom_field.allowed_values)))
            if self._custom_field.is_multi_value:
                for val in value:
                    _validate_select_value(val)
            else:
                _validate_select_value(val)
        return value

    def _transform_value(self):
        value = self._custom_field_value
        if Session.is_registered_endpoint(type(value)):
            value = value.key
        elif isinstance(value, datetime.date):
            value = value.strftime('%Y-%m-%d')
        return value

    def serialize(self):
        return {self._custom_field.key: self._transform_value()}

    def __eq__(self, other):
        return self.phone_number == other.phone_number and self.phone_type == other.phone_type

    def __ne__(self, other):
        return not self.__eq__(other)


class ContactCustomFieldValue(CustomFieldValueBase):
    pass


class CompanyCustomFieldValue(CustomFieldValueBase):
    pass


class CaseCustomFieldValue(CustomFieldValueBase):
    pass


class OpportunityCustomFieldValue(CustomFieldValueBase):
    pass


Session.register_endpoint(CustomField)
