import logging

from libs import APISession

logger = logging.getLogger(__name__)


def test_setting(settings):
    assert settings.session.base_url
    assert settings.session.time_out


def test_request(session):
    assert isinstance(session, APISession)


def test_mock(session):
    resp = session.get("https://mock.google.com")
    assert resp.status_code == 200
    assert resp.json()["code"] == 1

    resp = session.get("https://mock.baidu.com")
    assert resp.status_code == 200
    assert resp.json()["code"] == 2


def test_fetch(session):
    resp = session.get("http://m.baidu.com")
    assert "百度" in resp.text
