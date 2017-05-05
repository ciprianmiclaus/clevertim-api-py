import json
from clevertimapi.customfield import CustomField
from clevertimapi.session import Session
try:
    import unittest.mock as mock
except ImportError:
    import mock


def setup_requests_call_mock(requestsMockObj, config):
    prev_side_effect = requestsMockObj.side_effect

    def requests_call(*args, **kwargs):
        url = args[0]
        for endpoint, (status_code, response_text) in config.items():
            if url == Session.build_url(Session.ENDPOINT_URL, endpoint):
                mock_response = mock.Mock()
                mock_response.status_code = status_code
                mock_response.text = response_text
                return mock_response
        if prev_side_effect:
            return prev_side_effect(*args, **kwargs)
        else:
            raise LookupError("Cannot find a mock for requests.get for url:%s" % (url,))

    requestsMockObj.side_effect = requests_call


def generate_custom_field_info(key, name, field_type, field_scope, multiple, values=None):
    ret = {
        'status': 'OK',
        'content': [{
            'id': key,
            'name': name,
            'fullname': name,
            'elemType': field_type,
            'modelType': [field_scope],
            'multiple': multiple,
            'app': None
        }]
    }
    if values is not None:
        ret['content'][0]['values'] = values
    return json.dumps(ret)


def set_up_GET_custom_fields(requestsGETMockObj, field_scope):
    # cls.USER,
    # cls.CONTACT,
    # cls.COMPANY,
    # cls.CASE,
    # cls.OPPORTUNITY,
    setup_requests_call_mock(requestsGETMockObj, {
        '/customfield/1': (
            200,
            generate_custom_field_info(1, 'Input Custom Field', CustomField.FIELD_TYPE.INPUT, field_scope, False)
        ),
        '/customfield/2': (
            200,
            generate_custom_field_info(2, 'Select Custom Field', CustomField.FIELD_TYPE.SELECT, field_scope, False, values=['cf_value1', 'cf_value2', 'cf_value3', 'cf_value4'])
        ),
        '/customfield/3': (
            200,
            generate_custom_field_info(3, 'Date Custom Field', CustomField.FIELD_TYPE.DATE, field_scope, False)
        ),
        '/customfield/4': (
            200,
            generate_custom_field_info(4, 'Country Custom Field', CustomField.FIELD_TYPE.COUNTRY, field_scope, False)
        ),
        '/customfield/5': (
            200,
            generate_custom_field_info(5, 'State Custom Field', CustomField.FIELD_TYPE.STATE, field_scope, False)
        ),
        '/customfield/6': (
            200,
            generate_custom_field_info(6, 'Region Custom Field', CustomField.FIELD_TYPE.REGION, field_scope, False)
        ),
        '/customfield/7': (
            200,
            generate_custom_field_info(7, 'Currency Custom Field', CustomField.FIELD_TYPE.CURRENCY, field_scope, False)
        ),
    })
