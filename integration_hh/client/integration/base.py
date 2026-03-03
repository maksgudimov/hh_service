import os
import aiohttp
import asyncio
from typing import Union
from abc import ABC, abstractmethod
from starlette import status

from os import environ as environment
from pathlib import Path
from dotenv import load_dotenv
from common.enums import HttpMethod
from common import exceptions

env_path = os.path.join(Path(__file__).parent.parent.parent.parent, ".env")
load_dotenv(override=True, dotenv_path=env_path)


class BaseRequest(ABC):
    BASE_URL: str = "https://api.hh.ru/"
    ACCESS_TOKEN: str = environment["ACCESS_TOKEN_REQUEST"]

    def __init__(
            self,
            method: Union[HttpMethod.GET.value, HttpMethod.POST.value] = HttpMethod.GET.value,
            headers: dict = None,
            parameters: dict = None,
            path: str = None,
            *args,
            **kwargs,
    ):
        self.method = method
        self.headers = headers
        self.parameters = parameters
        self.path = path

    @property
    def get_headers(self):
        headers = self.headers
        headers.update(
            {
                "HH-User-Agent": "MyApp/1.0 (my-app-feedback@example.com)",
                "Authorization": f"Bearer {self.ACCESS_TOKEN}",
            }
        )

    @property
    def get_parameters(self):
        return self.parameters

    @property
    @abstractmethod
    def get_path(self):
        return self.path

    @property
    def url(self):
        return f"{self.BASE_URL}{self.get_path}"

    async def do_request(
            self,
    ):
        try:
            async with aiohttp.ClientSession() as session:
                if self.method == HttpMethod.GET.value:
                    async with session.get(
                        url=self.url,
                        params=self.get_parameters,
                        headers=self.headers,
                        timeout=10,
                    ) as response:
                        return await self.response_processing(response)
                else:
                    pass
        except aiohttp.ClientError as exp:
            raise exp
        except Exception as exp:
            raise exp

    @abstractmethod
    @staticmethod
    async def response_processing(
            response: aiohttp.ClientResponse
    ):
        pass
