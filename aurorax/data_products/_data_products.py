import datetime
import pprint
import aurorax
from aurorax.sources import DataSource
from pydantic import BaseModel
from typing import Dict, List, Optional

class DataProduct(BaseModel):
    """
    DataProduct data type

    :param data_source: data source that the ephemeris record is associated with
    :type data_source: aurorax.sources.DataSource
    :param data_product_type: data product type (keogram, movie, summary_plot)
    :param start: starting timestamp for the record in UTC
    :type start: datetime.datetime
    :param end: ending timestamp for the record in UTC
    :type end: datetime.datetime
    :param url: URL location of data product
    :type url: str
    :param metdata: metadata values for this record
    :type metdata: Dict
    """
    data_source: DataSource
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

        # format data source fields for query 
        d["program"] = self.data_source.program
        d["platform"] = self.data_source.platform
        d["instrument_type"] = self.data_source.instrument_type
        del d["data_source"]

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

def __validate_data_source(identifier: int, records: List[DataProduct]) -> Optional[DataProduct]:
        # get all current sources
        sources = {source.identifier: source for source in aurorax.sources.list()}
        if identifier not in sources.keys():
            raise aurorax.AuroraXValidationException(f"Data source with unique identifier {identifier} could not be found.")

        for record in records:
            # check the identifier, program name, platform name, and instrument type
            try:
                reference = sources[record.data_source.identifier]
            except KeyError:
                raise aurorax.AuroraXValidationException(f"Data source with unique identifier {record.data_source.identifier} could not be found.")

            if not (record.data_source.program == reference.program and 
                    record.data_source.platform == reference.platform and 
                    record.data_source.instrument_type == reference.instrument_type):
                return record

        return None


def upload(identifier: int, records: List[DataProduct], validate_source: bool = False) -> int:
    """
    Upload data product records to AuroraX

    :param identifier: data source ID
    :type identifier: int
    :param records: data product records to upload
    :type records: List[DataProduct]
    :param validate_source: Set to True to validate all records before uploading
    :type validate_source: bool, optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected content error
    :raises aurorax.AuroraXUploadException: upload error
    :raises aurorax.AuroraXValidationException: data source validation error


    :return: 1 for success, raises exception on error
    :rtype: int
    """
    # validate record sources if the flag is set
    if validate_source:
        validation_error = __validate_data_source(identifier, records)
        if validation_error:
            raise aurorax.AuroraXValidationException(f"Unable to validate data source found in record: {validation_error}")
 
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
        if type(res.data) is list:
            raise aurorax.AuroraXUploadException("%s - %s" % (res.status_code, res.data[0]["error_message"]))

        raise aurorax.AuroraXUploadException("%s - %s" % (res.status_code, res.data["error_message"]))

    # return
    return 1

def delete(data_source: DataSource, urls: List[str]) -> int:
    """
    Delete a range of data product records. This method is asynchronous.

    :param data_source: data source that the ephemeris record is associated with. Identifier, program, platform, and instrument_type are required.
    :type data_source: aurorax.sources.DataSource
    :param urls: URLs of data products to delete
    :type urls: List[str]

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXBadParametersException: invalid or missing parameters
    :raises aurorax.AuroraXNotFoundException: source not found
    :raises aurorax.AuroraXUnauthorizedException: invalid API key for this operation

    :return: 1 on success
    :rtype: int
    """
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise aurorax.AuroraXBadParametersException("One or more required data source parameters are missing. Delete operation aborted.")

    # do request
    url = aurorax.api.urls.data_products_upload_url.format(data_source.identifier)
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "urls": urls
    }
    delete_req = aurorax.AuroraXRequest(method="delete", url=url, body=params, null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        if type(res.data) is list:
            raise aurorax.AuroraXBadParametersException("%s - %s" % (res.status_code, res.data[0]["message"]))  
        raise aurorax.AuroraXBadParametersException("%s - %s" % (res.status_code, res.data["message"]))
    elif (res.status_code == 404):
        raise aurorax.AuroraXNotFoundException("%s - %s" % (res.status_code, res.data["message"]))

    # return
    return 1
    