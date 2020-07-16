import json
import requests
import datetime

API_CONJUNCTION_URL = "http://api.staging.aurorax.space:8080/api/v1/conjunctions/search"


def search(start_datetime, end_datetime, source_list=None, distance=500, conjunction_type="nbtrace"):
    """
    Search for conjunctions between a GroundInstrument and SpaceInstrument.
    """
    # check for valid start and end datetimes
    if not isinstance(start_datetime, datetime.datetime) or not isinstance(end_datetime, datetime.datetime) or start_datetime > end_datetime:
        print("Start and end datetimes are invalid")
        return -1
    
    # check for valid conjunction type
    if conjunction_type not in ["nbtrace", "sbtrace", "both"]:
        print("Invalid conjunction type specified. Try again.")
        return -1
    
    if not(type(distance) is int or type(distance) is float or distance < 0):
        print("Invalid distance specified: must enter a positive number. Try again.")
        return -1
    
    # check for valid objects in source list
    if source_list is None:
        print("No sources were specified. Try again.")
        return -1
    elif all(isinstance(source, GroundInstrument) or isinstance(source, SpaceInstrument) for source in source_list):
        print("All sources are valid classes.")
    else:
        print("Invalid source list. Try again.")
        return -1
    
    conjunction_params = {
        "e1": {
            "programs": [source_list[0].program] if source_list[0].program is not None else [],
            "platforms": [source_list[0].platform] if source_list[0].platform is not None else [],
            "instrument_types": [source_list[0].instrument_type] if source_list[0].instrument_type is not None else [],
            "metadata_filters": []
            },
        "e2": {
            "programs": [source_list[1].program] if source_list[0].program is not None else [],
            "platforms": [source_list[1].platform] if source_list[0].platform  is not None else [],
            "instrument_types": [source_list[1].instrument_type] if source_list[0].instrument_type  is not None else [],
            "metadata_filters": []
            },
        "start": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "conjunction_types": ["nbtrace", "sbtrace"] if conjunction_type == "both" else [conjunction_type],
        "max_distance": distance,
        }
    
    # process each metadata filter
    for index in range(len(source_list)):
        if source_list[index].metadata_filters is not None and source_list[index].metadata_filters != []:
            if isinstance(source_list[index].metadata_filters, str):
                # split it by operator
                i = source_list[index].metadata_filters.find("=")
                if i != -1:
                    key = source_list[index].metadata_filters[:i]
                    value = source_list[index].metadata_filters[i + 1:]
                    
                    # add this filter to the list of metadata filters
                    conjunction_params["e" + str(index + 1)]["metadata_filters"].append({"key": key, "operator": "=", "values": [value]})

                else:
                    print("Metadata error: '" + source_list[index].metadata_filters + "' key and value could not be found. Try again.")
                    return -1
                
            elif isinstance(source_list[index].metadata_filters, list) and all(isinstance(f, str) for f in source_list[index].metadata_filters):
                for f in source_list[index].metadata_filters:
                    # split it by "=" operator
                    i = f.find("=")
                    if i != -1:
                        key = f[:i]
                        value = f[i + 1:]
                        
                        # add this filter to the list of metadata filters
                        conjunction_params["e" + str(index + 1)]["metadata_filters"].append({"key": key, "operator": "=", "values": [value]})

                    else:
                        print("Metadata error: '" + f + "' key and value could not be found. Try again.")
                        return -1

    print(conjunction_params)
    
    search_result = requests.post(API_CONJUNCTION_URL, headers={"accept": "application/json", "Content-Type": "application/json"}, json=conjunction_params)
    if search_result.status_code == 200:
        results = json.loads(search_result.text)
    else:
        print("An API error occurred. Status code " + str(search_result.status_code) + ": " + search_result.text)
        results = -1
    
    return results


class GroundInstrument:
    """
    GroundInstrument(program, platform, instrument_type, metadata_filters)
    
    Represents a ground-based ephemeris source.
    """

    def __init__(self, program=None, platform=None, instrument_type=None, metadata_filters=None):
        # add checks for validity
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        self.metadata_filters = metadata_filters
        

class SpaceInstrument:
    """
    SpaceInstrument(program, platform, instrument_type, metadata_filters)
    
    Represents a space-based ephemeris source.
    """

    def __init__(self, program=None, platform=None, instrument_type=None, metadata_filters=None):
        # add checks for validity
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        self.metadata_filters = metadata_filters
