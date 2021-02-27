from ._api import AuroraXRequest
from ._api import get_api_key
from ._api import authenticate
from ._api import DEFAULT_RETRIES
from ._api import REQUEST_HEADERS
from ._api import API_KEY_HEADER_NAME

from ._urls import DEFAULT_URL_BASE
from ._urls import URLs

# create instance of URLs that will be used throughout the application
urls = URLs()


def set_base_url(url: str) -> None:
    """
    Change the base URL for the API (ie. change to the staging system or local server)

    :param url: new base url (ie. 'https://api.staging.aurorax.space')
    :type url: str
    """
    urls.base_url = url


def reset_base_url() -> None:
    """
    Set the base URL for the API back to the default
    """
    urls.base_url = DEFAULT_URL_BASE
