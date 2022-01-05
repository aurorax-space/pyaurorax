import pprint
from pydantic import BaseModel
from typing import List, Dict

# pdoc init
__pdoc__: Dict = {}


class DataSource(BaseModel):
    """
    Data source data type

    Attributes:
        identifier: an integer unique to the data source
        program: a string representing the data source program
        platform: a string representing the data source platform
        instrument_type: a string representing the data source instrument type
        source_type: a string representing the data source type
        display_name: a string representing the data source's proper display name
        metadata: a dictionary of metadata properties
        owner: a string representing the data source's owner in AuroraX
        maintainers: a list of strings representing the email addresses of AuroraX
            accounts that can alter this data source and its associated records
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in ephemeris records associated with
            the data source
        data_product_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in data product records associated with
            the data source
    """
    identifier: int = None
    program: str = None
    platform: str = None
    instrument_type: str = None
    source_type: str = None
    display_name: str = None
    metadata: Dict = None
    owner: str = None
    maintainers: List[str] = None
    ephemeris_metadata_schema: List[Dict] = None
    data_product_metadata_schema: List[Dict] = None

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of DataSource object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of DataSource object
        """
        return pprint.pformat(self.__dict__)
