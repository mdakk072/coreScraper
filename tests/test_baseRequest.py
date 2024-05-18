import pytest
from requests.exceptions import HTTPError
from core.baseRequest import BaseRequest
import requests_mock
import time

@pytest.fixture
def base_request():
    """Fixture to create a BaseRequest instance for testing."""
    proxies = ['http://proxy1.com', 'http://proxy2.com']
    user_agents = ['Mozilla/5.0 (Windows NT 10.0)', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)']
    return BaseRequest(base_url="http://example.com", proxies=proxies, user_agents=user_agents)

def test_request_with_user_agent_rotation(base_request):
    with requests_mock.Mocker() as m:
        m.get('http://example.com/test', text='response success')
        first_response = base_request.send_request('GET', '/test')
        second_response = base_request.send_request('GET', '/test')
        assert first_response.request.headers['User-Agent'] != second_response.request.headers['User-Agent'], "User-Agent should rotate between requests"

def test_get_success(base_request):
    with requests_mock.Mocker() as m:
        m.get('http://example.com/test', text='response success')
        response = base_request.send_request('GET', '/test')
        assert response.text == 'response success'

def test_post_success(base_request):
    with requests_mock.Mocker() as m:
        m.post('http://example.com/test', text='post success')
        response = base_request.send_request('POST', '/test', json={'key': 'value'})
        assert response.text == 'post success'

def test_request_failure(base_request):
    with requests_mock.Mocker() as m:
        m.get('http://example.com/test', status_code=500)
        with pytest.raises(HTTPError):
            base_request.send_request('GET', '/test')

def test_delay_action(base_request, mocker):
    mocker.spy(time, 'sleep')
    base_request.delay_action(min_delay=1, max_delay=1)
    assert time.sleep.called
    assert time.sleep.call_args[0][0] == 1, "Sleep should be called with exactly 1 second for both min and max delay set to 1"

def test_close_session(base_request, mocker):
    mocker.patch.object(base_request.session, 'close')
    base_request.close()
    assert base_request.session.close.called, "Session close method should be called"
