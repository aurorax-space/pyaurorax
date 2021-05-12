import datetime
import pprint
import aurorax
from pydantic import BaseModel
from typing import Dict, List, Optional


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

        # remove identifier
        del d["identifier"]

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


def __validate_data_source(records: List["DataProduct"]) -> Optional[DataProduct]:
        # get all current sources
        sources = {source["identifier"]: source for source in aurorax.sources.list()}

        for record in records:
            # check the identifier, program name, platform name, and instrument type
            try:
                reference = sources[record.identifier]
            except KeyError:
                raise aurorax.AuroraXValidationException("Data source with unique identifier {} could not be found.".format(record.identifier))

            if not (record.program == reference["program"] and record.platform == reference["platform"] and record.instrument_type == reference["instrument_type"]):
                return record

        return None


def upload(identifier: int, records: List["DataProduct"], validate_source: bool = False) -> int:
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


    :return: 0 for success, raises exception on error
    :rtype: int
    """
        # validate record sources if the flag is set
    if validate_source:
        validation_error = __validate_data_source(records)
        if validation_error:
            raise aurorax.AuroraXValidationException("Unable to validate data source found in record: {}".format(validation_error))
 

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
