import logging

from libs import APISession

logger = logging.getLogger(__name__)


def test_setting(settings):
    assert settings.session.base_url
    assert settings.session.time_out


def test_request(api_client):
    assert isinstance(api_client, APISession)


def test_mock(api_client):
    resp = api_client.get("https://mock.google.com")
    assert resp.status_code == 200
    assert resp.json()["code"] == 1

    resp = api_client.get("https://mock.baidu.com")
    assert resp.status_code == 200
    assert resp.json()["code"] == 2


def test_fetch(api_client):
    resp = api_client.get("http://m.baidu.com")
    assert "百度" in resp.text
