import logging

import pytest
from libs import APISession

logger = logging.getLogger(__name__)


def test_setting(settings):
    assert settings.session.base_url
    assert settings.session.time_out


def test_request(api_client):
    assert isinstance(api_client, APISession)


def test_request_baseurl(api_client):
    base_url = "https://api.tttt.one/rest-v2/"
    url = "/login/access_token"
    api_client.base_url = base_url
    resp = api_client.get(url, allow_redirects=False)
    assert resp.url.startswith(api_client.base_url)
    assert resp.url.endswith(url)


@pytest.mark.parametrize(
    "data",
    [
        ("", "http://baidu.com/b", "http://baidu.com/b"),
        ("http://m.baidu.com", "http://baidu.com/b", "http://baidu.com/b"),
        ("http://baidu.com", "/a", "http://baidu.com/a"),
        ("http://baidu.com/", "/a", "http://baidu.com/a"),
        ("http://baidu.com/a", "/a", "http://baidu.com/a/a"),
        ("http://baidu.com/a/", "/a", "http://baidu.com/a/a"),
    ],
)
def test_request_urljoin(api_client, data):
    base_url, url, new_url = data
    api_client.base_url = base_url
    resp = api_client.get(url, allow_redirects=False)

    assert resp.url == new_url


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
