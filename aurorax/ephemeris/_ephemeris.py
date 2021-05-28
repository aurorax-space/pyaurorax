import datetime
import pprint
import aurorax
from aurorax.sources import DataSource
from pydantic import BaseModel
from typing import Dict, List, Optional
from aurorax import Location

class Ephemeris(BaseModel):
    """
    Ephemeris data type

    :param data_source: data source that the ephemeris record is associated with
    :type data_source: aurorax.sources.DataSource
    :param epoch: timestamp for the record in UTC
    :type epoch: datetime.datetime
    :param location_geo: latitude and longitude in geographic coordinates
    :type location_geo: Location
    :param location_gsm: latitude and longitude in GSM coordinates (leave empty for
                         data sources with a type of 'ground')
    :type location_gsm: Location
    :param nbtrace: north B-trace geomagnetic latitude and longitude
    :type nbtrace: Location
    :param sbtrace: south B-trace geomagnetic latitude and longitude
    :type sbtrace: Location
    :param metadata: metadata values for this record
    :type metadata: Dict
    """
    data_source: DataSource
    epoch: datetime.datetime
    location_geo: Location
    location_gsm: Location
    nbtrace: Location
    sbtrace: Location
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
        if (type(d["epoch"]) is datetime.datetime):
            d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format location
        if (type(d["location_geo"]) is Location):
            d["location_geo"] = d["location_geo"].__dict__
        if (type(d["location_gsm"]) is Location):
            d["location_gsm"] = d["location_gsm"].__dict__
        if (type(d["nbtrace"]) is Location):
            d["nbtrace"] = d["nbtrace"].__dict__
        if (type(d["sbtrace"]) is Location):
            d["sbtrace"] = d["sbtrace"].__dict__

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

def __validate_data_source(identifier: int, records: List[Ephemeris]) -> Optional[Ephemeris]:
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

def upload(identifier: int, records: List[Ephemeris], validate_source: bool = False) -> int:
    """
    Upload ephemeris records to AuroraX

    :param identifier: data source ID
    :type identifier: int
    :param records: Ephemeris records to upload
    :type records: List[Ephemeris]
    :param validate_source: Set to True to validate all records before uploading. This will 
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
            raise aurorax.AuroraXValidationException("Unable to validate data source found in record: {}".format(validation_error))
    
    # translate each ephemeris record to a request-friendly dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(records):
        if (type(records[i]) is Ephemeris):
            records[i] = records[i].to_json_serializable()

    # make request
    url = aurorax.api.urls.ephemeris_upload_url.format(identifier)
    req = aurorax.AuroraXRequest(method="post", url=url, body=records, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise aurorax.AuroraXUploadException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 202):
        print("Status code 202, stream accepted")
    
    # return
    return 1

def delete(data_source: DataSource, start: datetime.datetime, end: datetime.datetime) -> int:
    """
    Delete a range of ephemeris records. This method is asynchronous.

    :param data_source: data source that the ephemeris record is associated with. Identifier, program, platform, and instrument_type are required.
    :type data_source: aurorax.sources.DataSource
    :param start: start datetime of deletion range
    :type start: datetime.datetime
    :param end: end datetime of deletion range
    :type end: datetime.datetime

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
    url = aurorax.api.urls.ephemeris_upload_url.format(data_source.identifier)
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S")
    }
    delete_req = aurorax.AuroraXRequest(method="delete", url=url, body=params, null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        if type(res.data) is list:
            raise aurorax.AuroraXBadParametersException("%s - %s" % (res.status_code, res.data[0]["message"]))  
        raise aurorax.AuroraXBadParametersException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 404):
        raise aurorax.AuroraXNotFoundException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 1
    