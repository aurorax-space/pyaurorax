"""
Class definition used for managing the response from an
API request
"""

from pydantic import BaseModel
from typing import Dict, Any

# pdoc init
__pdoc__: Dict = {}


class AuroraXResponse(BaseModel):
    """
    AuroraX API response class

    Attributes:
        request: the request object
        data: the data received as part of the request
        status_code: the HTTP status code received when making the request
    """
    request: Any
    data: Any
    status_code: int

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of AuroraXResponse
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of AuroraXResponse
        """
        return f"AuroraXResponse [{self.status_code}]"
