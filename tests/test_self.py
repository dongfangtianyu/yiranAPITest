import logging

logger = logging.getLogger(__name__)


def test_setting(settings):
    print(settings.base_url)
    print(settings.time_out)


def test_request(session):
    logger.info("x")


def test_mock(session):
    resp = session.get("https://google.com")
    assert resp.status_code == 200
    assert resp.json()["code"] == 1

    resp = session.get("https://baidu.com")
    assert resp.status_code == 200
    assert resp.json()["code"] == 2


def test_fetch(session):
    resp = session.get("http://m.baidu.com")
    assert "百度" in resp.text
