import logging
import logging.config
from typing import Dict

import pytest
import yaml

from libs import ApiInfo, APISession, Settings


@pytest.fixture(scope="session")
def settings():
    """加载配置文件"""

    with open("settings.yaml", encoding="utf-8") as f:
        conf = yaml.safe_load(f)

    logging.config.dictConfig(conf.pop("logging"))

    settings = Settings(**conf)
    return settings


@pytest.fixture()
def session(settings):
    """为每个测试用例创建一个session"""
    session = APISession(**settings.session.dict())
    for rule in settings.mocks:
        print(rule.dict())
        session.add_mock(**rule.dict())
    return session


@pytest.fixture()
def apis() -> Dict[str, ApiInfo]:
    """返回接口信息"""
    apis: Dict[str, ApiInfo] = {
        "get_token": ApiInfo(
            method="GET",
            url="/user/login",
        ),
        "post_login": ApiInfo(
            method="post",
            url="/user/login",
        ),
    }
    return apis


def pytest_runtest_setup(item):
    logger = logging.getLogger(__name__)
    logger.info(f"Start: {item.nodeid}".center(60, "-"))


def pytest_runtest_teardown(item):
    logger = logging.getLogger(__name__)
    logger.info(f"End: {item.nodeid}".center(60, "-"))
