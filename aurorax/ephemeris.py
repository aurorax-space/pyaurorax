import copy
import json
import aacgmv2
import requests
import datetime


def get_ephemeris_sources(program=None, platform=None, instrument_type=None, source_type=None, owner=None, format="basic_info"):
    """
    Returns a list of dictionaries representing all ephemeris sources.
    
    :param program: program name to filter sources by, optional
    :param platform: platform name to filter sources by, optional
    :param instrument_type: instrument type to filter sources by, optional
    :param source_type: source type to filter sources by (e.g. "heo"), optional
    :param owner: owner ID to filter sources by, optional
    :param format: the format of the ephemeris source returned Available values: "identifier_only", "basic_info", "full_record". Defaults to "basic_info". 
    
    :return: a dictionary of all ephemeris sources.
    """
    
    API_EPHEMERIS_SOURCES_URL = "http://api.staging.aurorax.space:8080/api/v1/ephemeris-sources"
    filters = {"program": program, "platform": platform, "instrument_type": instrument_type, "source_type": source_type, "owner": owner, "format": format}
    r = requests.get(API_EPHEMERIS_SOURCES_URL, params=filters)
    ephemeris_response = eval(r.text)
    
    return ephemeris_response


class GroundInstrument:
    """
    GroundInstrument(program, platform, instrument_type)
    
    Represents a ground-based ephemeris source.
    
    :var program: the instrument's program
    :var platform: the instrument's platform
    :var instrument_type: the instrument's type
    """

    def __init__(self, program=None, platform=None, instrument_type=None):
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        

class SpaceInstrument:
    """
    SpaceInstrument(program, platform, instrument_type)
    
    Represents a space-based ephemeris source.
    
    :var program: the instrument's program
    :var platform: the instrument's platform
    :var instrument_type: the instrument's type
    """

    def __init__(self, program=None, platform=None, instrument_type=None):
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type


class EphemerisRecord:
    """
    Represents an AuroraX ephemeris record.
    
    :var ephemeris_source_identifier: ID of the instrument's Aurorax ephemeris source
    :var program: the instrument's program
    :var platform: the instrument's platform
    :var instrument_type: the instrument's type
    :var epoch: datetime object representing the record's time of occurrence
    :var geo_lat: the instrument's geographic latitude. Use with geo_lon, or use location_geo dictionary
    :var geo_lon: the instrument's geographic longitude. Use with geo_lat, or use location_geo dictionary
    :var gsm_lat: the instrument's GSM latitude. Use with gsm_lon, or use location_gsm dictionary
    :var gsm_lon: the instrument's GSM longitude. Use with gsm_lat, or use location_gsm dictionary
    :var nbtrace_lat: the instrument's north B trace geographic latitude. Use with nbtrace_lon, or use nbtrace dictionary
    :var nbtrace_lon: the instrument's north B trace geographic longitude. Use with nbtrace_lat, or use nbtrace dictionary
    :var sbtrace_lat: the instrument's south B trace geographic latitude. Use with sbtrace_lon, or use sbtrace dictionary
    :var sbtrace_lon: the instrument's south B trace geographic longitude. Use with sbtrace_lat, or use sbtrace dictionary
    :var location_geo: the instrument's geographic coordinates in a dictionary in the form {"lat: <LATITUDE>, "lon": <LONGITUDE>}
    :var location_gsm: the instrument's GSM coordinates in a dictionary in the form {"lat: <LATITUDE>, "lon": <LONGITUDE>}
    :var nbtrace: the instrument's north B trace geographic coordinates in a dictionary in the form {"lat: <LATITUDE>, "lon": <LONGITUDE>}
    :var sbtrace: the instrument's south B trace coordinates in a dictionary in the form {"lat: <LATITUDE>, "lon": <LONGITUDE>}
    :var metadata: the instrument's metadata dictionary
    :var record: the ephemeris record's fields in AuroraX dictionary format 
    """

    def __init__(self, program=None, platform=None, instrument_type=None, epoch=None, geo_lat=None, geo_lon=None, gsm_lat=None, gsm_lon=None,
                 nbtrace_lat=None, nbtrace_lon=None, sbtrace_lat=None, sbtrace_lon=None, metadata=None, ephemeris_source_identifier=None,
                 location_geo=None, location_gsm=None, nbtrace=None, sbtrace=None):
        
        self.ephemeris_source_identifier = ephemeris_source_identifier
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        if type(epoch) is str:
            self.epoch = datetime.datetime.strptime(epoch, "%Y-%m-%dT%H:%M:%S")
        else:
            self.epoch = epoch
        if location_geo is None:
            self.geo_lat = geo_lat
            self.geo_lon = geo_lon
        else:
            self.geo_lat = location_geo["lat"]
            self.geo_lon = location_geo["lon"]
        if location_gsm is None:
            self.gsm_lat = gsm_lat
            self.gsm_lon = gsm_lon
        else:
            self.gsm_lat = location_gsm["lat"]
            self.gsm_lon = location_gsm["lon"]
        if nbtrace is None: 
            self.nbtrace_lat = nbtrace_lat
            self.nbtrace_lon = nbtrace_lon
        else:
            self.nbtrace_lat = nbtrace["lat"]
            self.nbtrace_lon = nbtrace["lon"]
        if sbtrace is None:
            self.sbtrace_lat = sbtrace_lat
            self.sbtrace_lon = sbtrace_lon
        else:
            self.sbtrace_lat = sbtrace["lat"]
            self.sbtrace_lon = sbtrace["lon"]
        self.metadata = metadata
        
    def to_dictionary(self):
        """
        Returns a copy of the EphemerisRecord as a dictionary in the AuroraX record format.
        """
        self.record = {
                        "ephemeris_source_identifier": self.ephemeris_source_identifier,
                        "program": self.program,
                        "platform": self.platform,
                        "instrument_type": self.instrument_type,
                        "epoch": self.epoch,
                        "location_geo": {"lat": self.geo_lat, "lon": self.geo_lon},
                        "location_gsm": {"lat": self.gsm_lat, "lon": self.gsm_lon},
                        "nbtrace": {"lat": self.nbtrace_lat, "lon": self.nbtrace_lon},
                        "sbtrace": {"lat": self.sbtrace_lat, "lon": self.sbtrace_lon},
                        "metadata": self.metadata
                    }
        
        return copy.deepcopy(self.record)


class EphemerisSearch:
    """
    A class for searching ephemeris records.
    
    :var start: a datetime object representing the search window's start
    :var end: a datetime object representing the seach window's end
    :var programs: a list of strings representing the programs to search
    :var platforms: a list of strings representing the platforms to search
    :var instrument_types: a list of strings representing the types of instrument to search
    :var metadata_filters: a list of dictionaries representing metadata filters for the ground instrument
        in the form {"key": <key>, "operator": <operator>, "value": <value>}. E.g. {"key": "temperature", "operator": "=", "value": 25.0}
    """

    def __init__(self, programs=None, platforms=None, instrument_types=None, metadata_filters=None, start=None, end=None):
        self.API_EPHEMERIS_SEARCH_URL = "http://api.staging.aurorax.space:8080/api/v1/ephemeris/search"
        
        self.start = start
        self.end = end
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.metadata_filters = metadata_filters

    def execute(self):
        """
        Executes the search with the given parameters.
        
        :return: a list of EphemerisRecord objects matching the search criteria, or an empty list if the search returned no records, or -1 if an error occurred
        """
        dict = self.to_dictionary()
        for key in list(dict["ephemeris_sources"].keys()):
            if dict["ephemeris_sources"][key] is None:
                dict["ephemeris_sources"].pop(key)
                
        search_result = requests.post(self.API_EPHEMERIS_SEARCH_URL, headers={"accept": "application/json", "Content-Type": "application/json"}, json=dict)
        if search_result.status_code == 200:
            results_dict = json.loads(search_result.text)["ephemeris_data"]
            self.results = []
            
            for r in results_dict:
                self.results.append(EphemerisRecord(**r))
            
        else:
            print("An API error occurred. Try Again.")
            print(search_result.text)
            self.results = -1
        
        return self.results
    
    def to_dictionary(self):
        """
        Returns a copy of the search parameters as a dictionary in the AuroraX ephemeris search format.
        """
        dict = {
        "ephemeris_sources": {
            "programs": self.programs,
            "platforms": self.platforms,
            "instrument_types": self.instrument_types,
            "metadata_filters": self.metadata_filters
            },
            "start": self.start.strftime("%Y-%d-%mT%H:%M:%S"),
            "end": self.end.strftime("%Y-%d-%mT%H:%M:%S")
        }
        return copy.deepcopy(dict)
        

class EphemerisUpload:
    """
    A class for uploading ephemeris records.
    
    :var ephemeris_sources: a list of dictionary objetcs, each representing an AuroraX ephemeris source. Identical to the result of get_ephemeris_sources()
    :var record_list: a list of EphemerisRecord objects to be uploaded
    :var api_key: the user's unique API key used for uploading ephemeris records to AuroraX. See the API for instructions on generating an API key
    """

    def __init__(self, api_key=None):
        self.API_EPHEMERIS_UPLOAD_URL = "http://api.staging.aurorax.space:8080/api/v1/ephemeris-sources/{}/ephemeris"
        self.ephemeris_sources = get_ephemeris_sources()
        self.record_list = []
        self.api_key = api_key
    
    def add_record(self, record):
        """
        Add an EphemerisRecord object to be uploaded.
        
        :param record: an EphemerisRecord object
        :raise: ValueError if the record is not an EphemerisRecord object
        """
        
        if type(record) is EphemerisRecord:
            
            if record.program is None or record.platform is None or record.instrument_type is None or record.geo_lat is None or record.geo_lon is None:
                print("Record program, platform, instrument_type, geo_lat, or geo_lon is missing. Try again.")
                return -1
            
            upload_record_params = record.to_dictionary()
            
            if record.ephemeris_source_identifier is None:
                source_id = None
                for source in self.ephemeris_sources:
                    if source["program"] == record.program and source["platform"] == record.platform and source["instrument_type"] == record.instrument_type:
                        source_id = source["identifier"]
                        upload_record_params["ephemeris_source_identifier"] = source_id
                        print("source_id is " + str(source_id))
                        break
                if source_id is None:
                    print("No ephemeris source was found to match this program, platform and instrument type. Please check the data parameters and try again.")
                    return -1
            
            if record.nbtrace_lat is None or record.nbtrace_lon is None:
                # calculate AACGM coordinates
                if record.geo_lat >= 0:  # northern hemisphere
                    record_nbtrace_location = aacgmv2.convert_latlon(record.geo_lat, record.geo_lon, 0.0, record.epoch)  # geomagnetic coordinate
                            
                    # flip the geomagnetic latitude and convert back to geographic coordinates for the south B trace
                    record_sbtrace_location = aacgmv2.convert_latlon(record_nbtrace_location[0] * -1.0, record_nbtrace_location[1], 0.0, record.epoch, method_code="A2G")
                    
                else:  # southern hemisphere
                    record_sbtrace_location = aacgmv2.convert_latlon(record.geo_lat, record.geo_lon, 0.0, record_epoch)  # geomagnetic coordinate
                            
                    # flip the geomagnetic latitude and convert back to geographic coordinates for the north B trace
                    record_nbtrace_location = aacgmv2.convert_latlon(record_sbtrace_location[0] * -1.0, record_sbtrace_location[1], 0.0, record.epoch, method_code="A2G")

                upload_record_params["nbtrace"] = {"lat": record_nbtrace_location[0], "lon": record_nbtrace_location[1]}
                upload_record_params["sbtrace"] = {"lat": record_sbtrace_location[0], "lon": record_sbtrace_location[1]}
                
            print(upload_record_params)
            self.record_list.append(upload_record_params)
            
        else:
            raise ValueError("Error: record is not type EphemerisRecord.")
    
    def execute(self):
        """
        Sends all EphemerisRecord objects in the record_list to the API. A valid api_key variable must be defined.
        
        The record_list will *NOT* be cleared after execution of this method. Use the clear() method to clear the record_list.
        
        :return: 1 if all records were successfully uploaded, else returns the HTTP response returned on error
        """
        if self.api_key is None:
            print("A valid API key is required to upload ephemeris records. Set the api_key variable to your API key and try again.")
            return -1
        
        record_dictionary = {}
        
        for r in self.record_list:
            r_copy = copy.deepcopy(r)
            # set the epoch to string format
            try:
                r_copy["epoch"] = r_copy["epoch"].strftime("%Y-%m-%dT%H:%M:%S")
            except:
                pass
            
            if r_copy["ephemeris_source_identifier"] in record_dictionary:
                record_dictionary[r_copy["ephemeris_source_identifier"]].append(r_copy)
            else:
                record_dictionary[r_copy["ephemeris_source_identifier"]] = []
                record_dictionary[r_copy["ephemeris_source_identifier"]].append(r_copy)
                
        for source_id in record_dictionary:
            req = requests.post(self.API_EPHEMERIS_UPLOAD_URL.format(source_id),
                              headers={"accept": "application/json", "Content-Type": "application/json", "x-aurorax-api-key": self.api_key},
                              json=record_dictionary[source_id])
            if req.status_code != 202:
                print("Error occurred while sending data to the API for source ID " + str(source_id) + ".\nAborting.")
                return req
            
        return 1
        
    def clear(self):
        """
        Clears all records from record_list.
        """
        self.record_list = []
