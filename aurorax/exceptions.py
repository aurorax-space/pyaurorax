class AuroraXException(Exception):

    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if (response is not None and not self.request and hasattr(response, "request")):
            self.request = self.response.request
        super(AuroraXException, self).__init__(*args, **kwargs)


class AuroraXNotFoundException(AuroraXException):
    pass


class AuroraXDuplicateException(AuroraXException):
    pass


class AuroraXValidationException(AuroraXException):
    pass


class AuroraXDatabaseException(AuroraXException):
    pass


class AuroraXUnexpectedContentTypeException(AuroraXException):
    pass


class AuroraXMaxRetriesException(AuroraXException):
    pass


class AuroraXBadParametersException(AuroraXException):
    pass


class AuroraXUnauthorizedException(AuroraXException):
    pass


class AuroraXConflictException(AuroraXException):
    pass


class AuroraXUploadException(AuroraXException):
    pass
