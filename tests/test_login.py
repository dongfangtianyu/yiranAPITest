import logging
import re
from typing import Dict

import pandas as pd
import pytest
from libs import ApiInfo

logger = logging.getLogger(__name__)


@pytest.fixture(
    scope="session",
    params=pd.read_excel(
        "ddt/case_data.xlsx",
        sheet_name="test_login",
    ).values,
)
def case_data(request):
    return request.param


def test_login(api_client, apis: Dict[str, ApiInfo], case_data):
    """
    通过参数化测试测试登录接口
    """
    user_name, user_password, code, *case_info = case_data
    logger.info(f"{case_info}")
    api = apis["get_token"]
    login_security = re.findall(
        r'"login_security" value="(.*?)" />',
        api_client.request(api.method, api.url).text,
    )

    api = apis["post_login"]
    api.data = {
        "user_name": user_name,
        "user_password": user_password,
        "login_security": login_security,
    }
    req = api_client.request(
        api.method,
        api.url,
        data=api.data,
        allow_redirects=False,
    )

    assert int(code) == req.status_code
