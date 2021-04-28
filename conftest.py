import logging
import logging.config
from typing import Dict

import pandas
import pandas as pd
import pytest
import yaml

from libs import ApiInfo, APISession, Settings

# 加载全局日志配置
with open("conf/logging.yaml", encoding="utf-8") as f:
    logging.config.dictConfig(yaml.safe_load(f))


@pytest.fixture(scope="session")
def settings():
    """加载配置文件"""
    with open("conf/settings.yaml", encoding="utf-8") as f:
        settings = Settings(**yaml.safe_load(f))
    return settings


@pytest.fixture(scope="session")
def mock_rule():
    """加载mock规则"""
    with open("conf/api_mock.yaml", encoding="utf-8") as f:
        rule_list = list(yaml.safe_load_all(f))
    return rule_list


@pytest.fixture()
def session(settings, mock_rule):
    """为每个测试用例创建一个session"""
    session = APISession(**settings.dict())
    for rule in mock_rule:
        session.add_mock(**rule)
    return session


@pytest.fixture()
def apis() -> Dict[str, ApiInfo]:
    """为每个测试用例创建一个session"""
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
