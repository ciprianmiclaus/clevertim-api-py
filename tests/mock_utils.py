from clevertimapi.session import Session
try:
    import unittest.mock as mock
except ImportError:
    import mock


def setup_requests_call_mock(requestsMockObj, config):
    def requests_call(*args, **kwargs):
        url = args[0]
        for endpoint, (status_code, response_text) in config.iteritems():
            if url == Session.build_url(Session.ENDPOINT_URL, endpoint):
                mock_response = mock.Mock()
                mock_response.status_code = status_code
                mock_response.text = response_text
                return mock_response
        raise LookupError("Cannot find a mock for requests.get for url:%s" % (url,))

    requestsMockObj.side_effect = requests_call
