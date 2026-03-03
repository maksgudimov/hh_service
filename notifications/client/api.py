import aiohttp
from client.base import BaseRequest

class ApiClient(BaseRequest):
    # какой-то аналогичный клиент как в других модулях
    def __init__(self):
        pass

    @staticmethod
    async def response_processing(
            response: aiohttp.ClientResponse
    ):
        pass