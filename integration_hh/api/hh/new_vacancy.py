from typing import Annotated, Any, Union
from fastapi import Body, Request, Depends, HTTPException, Response
from starlette import status

from client.integration.hh import GetResumeRequest
from common.utils import check_token_hh
from producers.reaction_producer import rabbitmq_client
from shemas.request.hh_webhook.models import NewVacancyHHWebhook
from common import exceptions


async def add_new_vacancy(
        data: Annotated[NewVacancyHHWebhook, Body()],
        _: Annotated[Union[HTTPException, None], Depends(check_token_hh)]
):

    try:
        resume_obj = GetResumeRequest(data)
        resume_dict = await resume_obj.do_request()
    except Exception as exp:
        # какая-то обработка ошибок, кастомных в том числе из файла excpetion
        if type(exp) == Exception:
            pass
        else:
            pass
    else:
        # отправка в rabbit только в случае успеха и наличия данных
        success = await rabbitmq_client.publish_message(resume_dict)
        if success:
            return Response(status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
