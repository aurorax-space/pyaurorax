import datetime
import pprint
import aurorax
from pydantic import BaseModel
from typing import Dict, List, Optional
from aurorax import Location


class Ephemeris(BaseModel):
    """
    Ephemeris data type

    :param identifier: data source ID
    :type identifier: int
    :param program: program name
    :type program: str
    :param platform: platform name
    :type platform: str
    :param instrument_type: instrument type name
    :type instrument_type: str
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
    :param metdata: metadata values for this record
    :type metdata: Dict
    """
    identifier: int
    program: str
    platform: str
    instrument_type: str
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

def __validate_data_source(records: List["Ephemeris"]) -> Optional[Ephemeris]:
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

def upload(identifier: int, records: List["Ephemeris"], validate_source: bool = False) -> int:
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

    :return: 0 for success, raises exception on error
    :rtype: int
    """
    # validate record sources if the flag is set
    if validate_source:
        validation_error = __validate_data_source(records)
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
    return 0

def delete(identifier: int, program: str, platform: str, instrument_type: str, start: datetime.datetime, end: datetime.datetime) -> int:
    """
    Delete a range of ephemeris records. This method is asynchronous.

    :param identifier: data source identifier
    :type identifier: int
    :param program: program name
    :type program: str
    :param platform: platform name
    :type platform: str
    :param instrument_type: instrument type
    :type instrument_type: str
    :param start: start datetime of deletion range
    :type start: datetime.datetime
    :param end: end datetime of deletion range
    :type end: datetime.datetime

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXBadParametersException: invalid or missing parameters
    :raises aurorax.AuroraXNotFoundException: source not found
    :raises aurorax.AuroraXUnauthorizedException: invalid API key for this operation

    :return: 0 on success
    :rtype: int
    """
    # do request
    url = aurorax.api.urls.ephemeris_upload_url.format(identifier)
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S")
    }
    delete_req = aurorax.AuroraXRequest(method="delete", url=url, body=params, null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise aurorax.AuroraXBadParametersException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 404):
        raise aurorax.AuroraXNotFoundException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 0
    