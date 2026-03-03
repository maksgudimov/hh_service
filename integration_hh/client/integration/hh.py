import aiohttp
from starlette import status

from client.integration.base import BaseRequest
from shemas.request.hh_webhook.models import NewVacancyHHWebhook
from shemas.response.hh.get_resume.model import GetResumeModel
from common import exceptions
from common.enums import HttpMethod


class GetResumeRequest(BaseRequest):
    def __init__(
            self,
            method: HttpMethod = HttpMethod.GET.value,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.data: NewVacancyHHWebhook = kwargs["data"]
        self.method = method
        self.path = f"resumes/{self.data.id}"

    def get_parameters(self) -> dict:
        return {
            "with_negotiations_history": "true",
            "with_creds": "true",
            "with_job_search_status": "true",
            "host": "hh.ru",
            "locale": "RU",
        }

    @staticmethod
    async def response_processing(
            response: aiohttp.ClientResponse
    ) -> dict | Exception:
        if response.status == status.HTTP_200_OK:
            model_data = GetResumeModel.model_validate(response.json())
            return model_data.model_dump()
        elif response.status == status.HTTP_403_FORBIDDEN:
            raise exceptions.NonAuthorizedException403()
        elif response.status == status.HTTP_404_NOT_FOUND:
            raise exceptions.NotFoundException404()
        elif response.status == status.HTTP_429_TOO_MANY_REQUESTS:
            raise exceptions.LimitExceededException429()
        else:
            raise Exception()