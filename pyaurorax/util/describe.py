"""
Helper functions for describing different searches in
different ways.
"""

from typing import Dict
from ..api import AuroraXRequest, urls
from ..conjunctions import Search

# pdoc init
__pdoc__: Dict = {}


def describe_conjunction_search(search_obj: Search) -> str:
    """
    Represent a conjunction search as a "SQL-like" string

    Args:
        search_obj: the conjunction search object to describe

    Returns:
        the "SQL-like" string describing the conjunction search object
    """
    # make request
    req = AuroraXRequest(method="post",
                         url=urls.describe_conjunction_query,
                         body=search_obj.query)
    res = req.execute()

    # return
    return res.data


def describe_data_products_search(search_obj: Search) -> str:
    """
    Represent a data product search as a "SQL-like" string

    Args:
        search_obj: the data product search object to describe

    Returns:
        the "SQL-like" string describing the data product search object
    """
    # make request
    req = AuroraXRequest(method="post",
                         url=urls.describe_data_products_query,
                         body=search_obj.query)
    res = req.execute()

    # return
    return res.data


def describe_ephemeris_search(search_obj: Search) -> str:
    """
    Represent an ephemeris search as a "SQL-like" string

    Args:
        search_obj: the ephemeris search object to describe

    Returns:
        the "SQL-like" string describing the ephemeris search object
    """
    # make request
    req = AuroraXRequest(method="post",
                         url=urls.describe_ephemeris_query,
                         body=search_obj.query)
    res = req.execute()

    # return
    return res.data
