from starlette import status


class BaseApiException(Exception):
    pass


class NonAuthorizedException403(BaseApiException):
    status = status.HTTP_403_FORBIDDEN


class NotFoundException404(BaseApiException):
    status = status.HTTP_404_NOT_FOUND


class LimitExceededException429(BaseApiException):
    status = status.HTTP_429_TOO_MANY_REQUESTS
