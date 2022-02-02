"""
Helper functions when interacting with the API
"""

from typing import Dict
from .classes.urls import URLs
from ..api import DEFAULT_BASE_URL

# pdoc init
__pdoc__: Dict = {}

# private dynamic globals
__api_key: str = ""

# create instance of URLs that will be used throughout the application
urls = URLs()


def get_api_key() -> str:
    """
    Returns the currently set API key for the module

    Returns:
        current API key
    """
    return __api_key


def authenticate(api_key: str) -> None:
    """
    Set authentication values for use with subsequent queries

    Args:
        api_key: an AuroraX API key string
    """
    global __api_key
    __api_key = api_key


def set_base_url(url: str) -> None:
    """
    Change the base URL for the API (ie. change to the staging
    system or local server)

    Args:
        url: the new base url string (ie. 'https://api.staging.aurorax.space')
    """
    urls.base_url = url


def get_base_url() -> str:
    """
    Returns the current base URL for the API

    Returns:
        current base URL
    """
    return urls.base_url


def reset_base_url() -> None:
    """
    Set the base URL for the API back to the default
    """
    urls.base_url = DEFAULT_BASE_URL
