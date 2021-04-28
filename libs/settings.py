from pydantic import (AnyHttpUrl, BaseModel, BaseSettings, Field, PostgresDsn,
                      PyObject, RedisDsn)


class Settings(BaseSettings):
    base_url: AnyHttpUrl
    time_out: int = 5
