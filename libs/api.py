import logging
from dataclasses import dataclass, field
from typing import Text, Union
from urllib.parse import urljoin

import requests
import requests_mock
from requests import PreparedRequest, Response


class APISession(requests.Session):
    """
    为requests.Session证据BaseURL的功能，如果请求的相对路径，自动为其添加baseURL
    """

    base_url = None
    logger = logging.getLogger("requests.session")
    __mock: requests_mock.Mocker

    def __init__(self, base_url=None, time_out=None):
        self.base_url = base_url
        self.time_out = time_out
        self.__mock = requests_mock.Mocker(
            session=self,
            real_http=True,  # 未mock接口，是否正常放行
        )

        self.__mock.start()  # 开启mock功能
        self.logger.info("mock功能启动")
        super(APISession, self).__init__()

    def request(
        self, method: str, url: Union[str, bytes, Text], *args, **kwargs
    ) -> Response:
        if self.base_url:
            url = urljoin(self.base_url, url)
        return super(APISession, self).request(method, url, *args, **kwargs)

    def send(self, request: PreparedRequest, **kwargs) -> Response:
        """发送前记录requests， 响应后记录response"""
        self.logger.info(f"发送请求>>> 接口地址 = {request.method} {request.url}")
        self.logger.debug(f"发送请求>>> 请求头= {request.headers} ")
        self.logger.debug(f"发送请求>>> 请求正文= {request.body}")
        response = super(APISession, self).send(request, **kwargs)

        self.logger.info(f"接收响应<<< 状态码 = {response.status_code}")
        self.logger.debug(f"接收响应<<< 响应头= {response.headers} ")
        self.logger.debug(f"接收响应<<< 响应正文= {response.text}")

        return response

    def add_mock(self, request, response):
        """
        添加mock规则
        :param request: 要mock的目标
            {'method':'GET', 'url': 'https://google.com'}
        :param response: mock 结果
            {'status_code':200, 'headers':{”name":"sanmu"}, text='北京欢迎你'}
        :return:
        """
        self.__mock.request(**request, **response)
        self.logger.debug(f"添加了新规则{request} {response}")


@dataclass
class ApiInfo:
    """接口信息"""

    method: str  # 请求方式
    url: str  # 接口地址
    params: dict = field(default_factory=lambda: {})
    body: dict = field(default_factory=lambda: {})
    code: int = 200
    resp_body: dict = field(default_factory=lambda: {"code": 0, "data": "", "msg": ""})
