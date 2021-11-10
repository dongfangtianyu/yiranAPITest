from typing import Dict

import pytest
from libs import ApiInfo


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
