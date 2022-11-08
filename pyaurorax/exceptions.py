"""
The exceptions module contains exceptions unique to the PyAuroraX library
"""


class AuroraXException(Exception):

    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if (response is not None and not self.request and hasattr(response, "request")):
            self.request = self.response.request
        super(AuroraXException, self).__init__(*args, **kwargs)


class AuroraXNotFoundException(AuroraXException):
    """
    The AuroraX record was not found
    """
    pass


class AuroraXDuplicateException(AuroraXException):
    """
    A duplicate record already exists
    """
    pass


class AuroraXValidationException(AuroraXException):
    """
    Validation of data failed
    """
    pass


class AuroraXUnexpectedContentTypeException(AuroraXException):
    """
    The API responded with an unexpected content type
    """
    pass


class AuroraXMaxRetriesException(AuroraXException):
    """
    The maximum number of retries for the request has been reached
    """
    pass


class AuroraXBadParametersException(AuroraXException):
    """
    Bad parameters were given in the request
    """
    pass


class AuroraXUnauthorizedException(AuroraXException):
    """
    A privileged operation was attempted without authorization
    """
    pass


class AuroraXConflictException(AuroraXException):
    """
    A conflict occurred while modifying records
    """
    pass


class AuroraXUploadException(AuroraXException):
    """
    Error occurred during upload operation
    """
    pass


class AuroraXUnexpectedEmptyResponse(AuroraXException):
    """
    An empty response was received when it wasn't expected
    """
    pass


class AuroraXDataRetrievalException(AuroraXException):
    """
    Error occurred while retrieving search data
    """
    pass


class AuroraXTimeoutException(AuroraXException):
    """
    A timeout was reached while communicating with the AuroraX API
    """
    pass


class AuroraXSearchException(AuroraXException):
    """
    An error occured in the API while performing a search
    """
    pass
