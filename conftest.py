import logging
import logging.config
import os

import pytest
import yaml
from _pytest.config import Config

from libs import APISession, Settings
from libs.settings import AllureSettings

ALLURE_SETTINGS: AllureSettings
SETTINGS: Settings


@pytest.fixture(scope="session")
def settings():
    """加载配置文件"""
    return SETTINGS


@pytest.fixture()
def api_client(settings):
    """为每个测试用例创建一个session"""
    session = APISession(**settings.session.dict())
    for rule in settings.mocks:
        session.add_mock(**rule.dict())

    return session


def pytest_runtest_setup(item):
    logger = logging.getLogger(__name__)
    logger.info(f"Start: {item.nodeid}".center(60, "-"))


def pytest_runtest_teardown(item):
    logger = logging.getLogger(__name__)
    logger.info(f"End: {item.nodeid}".center(60, "-"))


def pytest_configure():
    global ALLURE_SETTINGS, SETTINGS
    with open("settings.yaml", encoding="utf-8") as f:
        conf = yaml.safe_load(f)

    logging.config.dictConfig(conf.pop("logging"))

    SETTINGS = Settings(**conf)

    ALLURE_SETTINGS = SETTINGS.report


def pytest_terminal_summary(config: Config):
    """准备输出报告"""
    allure_dir = config.getoption("allure_report_dir")

    os.system(
        f"{ALLURE_SETTINGS.allure_path}allure generate {allure_dir} -o"
        f" {ALLURE_SETTINGS.out_dir} --clean"
    )
