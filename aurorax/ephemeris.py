import json
import pytz
import aacgmv2
import requests
import datetime

API_EPHEMERIS_SEARCH_URL = "http://api.staging.aurorax.space:8080/api/v1/ephemeris/search"
API_EPHEMERIS_SOURCES_URL = "http://api.staging.aurorax.space:8080/api/v1/ephemeris-sources"
API_EPHEMERIS_UPLOAD_URL = "http://api.staging.aurorax.space:8080/api/v1/ephemeris-sources/{}/ephemeris"
API_KEY = None


def get_ephemeris_sources(program=None, platform=None, instrument_type=None, source_type=None, owner=None, format="basic_info"):
    """
    Returns a list of dictionaries representing all ephemeris sources.
    """
    filters = {"program": program, "platform": platform, "instrument_type": instrument_type, "source_type": source_type, "owner": owner, "format": format}
    r = requests.get(API_EPHEMERIS_SOURCES_URL, params=filters)
    ephemeris_response = eval(r.text)
    
    return ephemeris_response


def set_api_key(api_key):
    global API_KEY
    API_KEY = api_key


def search_instrument(instrument, start_datetime=None, end_datetime=None):
    """
    Search for ephemeris records
    """
    # check that both start and end datetimes were provided
    if not isinstance(start_datetime, datetime.datetime) or not isinstance(end_datetime, datetime.datetime) or start_datetime > end_datetime:
        print("Start and end datetimes are invalid")
        return -1
    elif not (isinstance(instrument, GroundInstrument) or isinstance(instrument, SpaceInstrument)):
        print("Instrument is not a valid GroundInstrument or SpaceInstrument class")
        return -1
    
    print(instrument.program, instrument.platform, instrument.instrument_type)
    
    search_params = {
        "ephemeris_sources": {
            "programs": [instrument.program],
            "platforms": [instrument.platform],
            "instrument_types": [instrument.instrument_type]
            },
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat()
        }
    
    search_result = requests.post(API_EPHEMERIS_SEARCH_URL, headers={"accept": "application/json", "Content-Type": "application/json"}, json=search_params)
    if search_result.status_code == 200:
        results = json.loads(search_result.text)
    else:
        print("An API error occurred. Status code " + str(search_result.status_code) + ": " + search_result.text)
        results = -1
    
    return results
    

def search(programs=None, platforms=None, instrument_types=None, metadata_filters=None, start_datetime=None, end_datetime=None):
    if not isinstance(start_datetime, datetime.datetime) or not isinstance(end_datetime, datetime.datetime) or start_datetime > end_datetime:
        print("Start and end datetimes are invalid")
        return -1
    
    search_params = {
        "ephemeris_sources": {
            "programs": [],
            "platforms": [],
            "instrument_types": [],
            "metadata_filters": []
            },
            "start": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        }
    
    # check filter parameters for validity
    for filter in [(programs, "programs"), (platforms, "platforms"), (instrument_types, "instrument_types")]:
        if isinstance(filter[0], list):
            for f in filter[0]:
                if not isinstance(f, str):
                    print("Invalid type in filter list. Try again.")
                    return -1
                else:
                    search_params["ephemeris_sources"][filter[1]].append(f)
        elif isinstance(filter, str):
            search_params["ephemeris_sources"][filter[1]].append(filter[0])
        elif filter[0] is None:
            pass
        else:
            print("Invalid type in filters list: programs, platforms, and instrument_types must be strings or lists of strings. Try again.")
            return -1
        
    # process each metadata filter
    if metadata_filters is not None and metadata_filters != []:
        if isinstance(metadata_filters, str):
            # split it by operator
            i = metadata_filters.find("=")
            if i != -1:
                key = metadata_filters[:i]
                value = metadata_filters[i + 1:]
                
                # add this filter to the list of metadata filters
                search_params["ephemeris_sources"]["metadata_filters"].append({"key": key, "operator": "=", "values": [value]})

            else:
                print("Metadata error: '" + metadata_filters + "' key and value could not be found. Try again.")
                return -1
            
        elif isinstance(metadata_filters, list) and all(isinstance(f, str) for f in metadata_filters):
            for f in metadata_filters:
                # split it by operator
                i = f.find("=")
                if i != -1:
                    key = f[:i]
                    value = f[i + 1:]
                    
                    # add this filter to the list of metadata filters
                    search_params["ephemeris_sources"]["metadata_filters"].append({"key": key, "operator": "=", "values": [value]})

                else:
                    print("Metadata error: '" + f + "' key and value could not be found. Try again.")
                    return -1
    
    search_result = requests.post(API_EPHEMERIS_SEARCH_URL, headers={"accept": "application/json", "Content-Type": "application/json"}, json=search_params)
    if search_result.status_code == 200:
        results = json.loads(search_result.text)
    else:
        print("An API error occurred. Try Again.")
        results = -1
    
    return results
    
    
def __process_record(data, metadata, source_id):
    ephemeris_record = {
                        "ephemeris_source_identifier": None,
                        "program": None,
                        "platform": None,
                        "instrument_type": None,
                        "epoch": None,
                        "location_geo": {
                            "lat": None,
                            "lon": None
                            },
                        "location_gsm": {
                            "lat": None,
                            "lon": None,
                            },
                        "nbtrace": {
                            "lat": None,
                            "lon": None
                            },
                        "sbtrace": {
                            "lat": None,
                            "lon": None
                            },
                        "metadata": metadata
                    }
    
    try:
        # check for valid data variables (program, platform, instrument_type, UTC date&time, latitude, longitude)
        ephemeris_record["ephemeris_source_identifier"] = source_id
        ephemeris_record["program"] = data["program"]
        ephemeris_record["platform"] = data["platform"]
        ephemeris_record["instrument_type"] = data["instrument_type"]
        
        try:
            record_epoch = datetime.datetime(data["year"], data["month"], data["day"], data["hour"], data["minute"], 0)
            ephemeris_record["epoch"] = record_epoch.isoformat()
        except Exception as de:
            print("Error: " + str(de))
            return -1
        
        if not (data["geo_lat"] >= -90 and data["geo_lat"] <= 90 and data["geo_lon"] >= -180 and data["geo_lon"] <= 180):
            print("Invalid GEO location parameter. Try again.")
            return -1
        else:
            ephemeris_record["location_geo"]["lat"] = data["geo_lat"]
            ephemeris_record["location_geo"]["lon"] = data["geo_lon"]
            
        # calculate AACGM coordinates
        if data["geo_lat"] >= 0:
            # northern hemisphere
            record_nbtrace_location = aacgmv2.convert_latlon(data["geo_lat"], data["geo_lon"], 0.0, record_epoch)  # geomagnetic coordinate
                    
            # flip the geomagnetic latitude and convert back to geographic coordinates for the south B trace
            record_sbtrace_location = aacgmv2.convert_latlon(record_nbtrace_location[0] * -1.0, record_nbtrace_location[1], 0.0, record_epoch, method_code="A2G")
        else:
            # southern hemisphere
            record_sbtrace_location = aacgmv2.convert_latlon(data["geo_lat"], data["geo_lon"], 0.0, record_epoch)  # geomagnetic coordinate
                    
            # flip the geomagnetic latitude and convert back to geographic coordinates for the north B trace
            record_nbtrace_location = aacgmv2.convert_latlon(record_sbtrace_location[0] * -1.0, record_sbtrace_location[1], 0.0, record_epoch, method_code="A2G")
        
        ephemeris_record["nbtrace"]["lat"] = record_nbtrace_location[0]
        ephemeris_record["nbtrace"]["lon"] = record_nbtrace_location[1]
        ephemeris_record["sbtrace"]["lat"] = record_sbtrace_location[0]
        ephemeris_record["sbtrace"]["lon"] = record_sbtrace_location[1]
    except Exception as e:
        print("Error: " + str(e))
        return -1
    
    return ephemeris_record

    
def upload(data, metadata=[]):
    """
    Upload a single ephemeris record to AuroraX.
    """
    # get the ephemeris source ID
    ids = get_ephemeris_sources()
    source_id = None
    
    for source in ids:
        if source["program"] == data["program"] and source["platform"] == data["platform"] and source["instrument_type"] == data["instrument_type"]:
            source_id = source["identifier"]
            print("source_id is " + source_id)
            break
    if source_id is None:
        print("No ephemeris source was found to match this program, platform and instrument type. Please check the data parameters and try again.")
        return -1
    
    record = __process_record(data, metadata, source_id)

    if record != -1:
        r = requests.post(API_EPHEMERIS_UPLOAD_URL.format(source_id), headers={"accept": "application/json", "Content-Type": "application/json", "x-aurorax-api-key": API_KEY}, json=record)
        return r


def upload_many(data_list, metadata_list):
    """
    Upload many ephemeris records to AuroraX.
    """
    if len(data_list) != len(metadata_list):
        print("The number of data records does not match the number of metadata records. Try again.")
        return -1
    elif not isinstance(data_list, list) or not isinstance(metadata_list, list):
        print("Data and metadata parameters must be lists. Try again.")
        return -1
    
    ids = get_ephemeris_sources()
    all_records = {}
    
    try:
        for i in range(len(data_list)):
            for source in ids:
                if source["program"] == data_list[i]["program"] and source["platform"] == data_list[i]["platform"] and source["instrument_type"] == data_list[i]["instrument_type"]:
                    source_id = source["identifier"]
                    break
            if source_id is None:
                print("No ephemeris source was found to match program, platform and instrument type at data list index " + str(i) + ". Please check the data parameters and try again.")
                return -1
            
            data = data_list[i]
            metadata = metadata_list[i]
            
            record = __process_record(data, metadata, source_id)
            
            if source_id not in all_records:
                all_records[source_id] = []
            
            if record != -1:
                all_records[source_id].append(record)
            else:
                print("Error encountered at data list index " + str(i) + ". Try again.")
                return -1
            
        for id in all_records:
            r = requests.post(API_EPHEMERIS_UPLOAD_URL.format(id), headers={"accept": "application/json", "Content-Type": "application/json", "x-aurorax-api-key": API_KEY}, json=all_records[id])
            if r.status_code != 202:
                print("Error occurred while sending data to the API for source ID " + str(id) + ".\nAborting.")
                return r
    except Exception as e:
        print("Error: " + str(e))
        return -1


class GroundInstrument:
    """
    GroundInstrument(program, platform, instrument_type)
    
    Represents a ground-based ephemeris source.
    """

    def __init__(self, program=None, platform=None, instrument_type=None):
        # add checks for validity
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        

class SpaceInstrument:
    """
    SpaceInstrument(program, platform, instrument_type[, id])
    
    Represents a space-based ephemeris source.
    """

    def __init__(self, program=None, platform=None, instrument_type=None):
        # add checks for validity
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
