import datetime
import pprint
import aurorax
from pydantic import BaseModel
from typing import Dict, List


class DataProduct(BaseModel):
    """
    DataProduct data type

    :param identifier: data source ID
    :type identifier: int
    :param program: program name
    :type program: str
    :param platform: platform name
    :type platform: str
    :param instrument_type: instrument type name
    :type instrument_type: str
    :param data_product_type: data product type (keogram, movie, summary_plot)
    :type instrument_type: str
    :param start: starting timestamp for the record in UTC
    :type start: datetime.datetime
    :param end: ending timestamp for the record in UTC
    :type end: datetime.datetime
    :param url: URL location of data product
    :type url: str
    :param metdata: metadata values for this record
    :type metdata: Dict
    """
    identifier: int
    program: str
    platform: str
    instrument_type: str
    data_product_type: str
    start: datetime.datetime
    end: datetime.datetime
    url: str
    metadata: Dict

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate datetime
        objects to strings)

        :return: dictionary JSON-serializable object
        :rtype: Dict
        """
        d = self.__dict__

        # format epoch as str
        if (type(d["start"]) is datetime.datetime):
            d["start"] = d["start"].strftime("%Y-%m-%dT%H:%M:00.000Z")
        if (type(d["end"]) is datetime.datetime):
            d["end"] = d["end"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format metadata
        if (type(self.metadata) is dict):
            for key, value in self.metadata.items():
                if (type(value) is datetime.datetime or type(value) is datetime.date):
                    self.metadata[key] = self.metadata[key].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if (type(self.metadata) is list):
            self.metadata = {}

        # return
        return d

    def __str__(self) -> str:
        """
        String method

        :return: string format
        :rtype: str
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return pprint.pformat(self.__dict__)


def upload(identifier: int, records: List["DataProduct"]) -> int:
    """
    Upload data product records to AuroraX

    :param identifier: data source ID
    :type identifier: int
    :param records: data product records to upload
    :type records: List[DataProduct]

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected content error
    :raises aurorax.AuroraXUploadException: upload error

    :return: 0 for success, raises exception on error
    :rtype: int
    """
    # translate each data product record to a request-friendly dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(records):
        if (type(records[i]) is DataProduct):
            records[i] = records[i].to_json_serializable()

    # make request
    url = aurorax.api.urls.data_products_upload_url.format(identifier)
    req = aurorax.AuroraXRequest(method="post", url=url, body=records, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise aurorax.AuroraXUploadException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 0
