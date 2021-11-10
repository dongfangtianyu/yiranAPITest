from enum import Enum
from http import HTTPStatus
from typing import List, Optional

from pydantic import AnyHttpUrl
from pydantic import BaseModel as PydanticBaseModel
from pydantic import BaseSettings


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

    def dict(self, **kwargs) -> dict:
        kwargs["by_alias"] = True
        return super().dict(**kwargs)


class _SessionSettings(BaseSettings):
    base_url: AnyHttpUrl
    time_out: int = 0


class HttpMethodEnum(str, Enum):
    GET = "GET"


class Request(BaseModel):
    method: str
    url: AnyHttpUrl


class Response(BaseModel):
    status_code: HTTPStatus
    headers: Optional[dict] = {}
    json_: dict

    class Config:
        fields = {"json_": "json"}


class MockRule(BaseModel):
    request: Request
    response: Response


class Settings(BaseSettings):
    session: _SessionSettings
    mocks: List[MockRule]
