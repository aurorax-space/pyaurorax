import copy
import json
import requests
import datetime

"""
def search(start_datetime, end_datetime, source_list=None, distance=500, conjunction_type="nbtrace"):
    '''
    Search for conjunctions between a GroundInstrument and SpaceInstrument.
    '''
    API_CONJUNCTION_URL = "http://api.staging.aurorax.space:8080/api/v1/conjunctions/search"
    
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
        "source1": {
            "programs": [source_list[0].program] if source_list[0].program is not None else [],
            "platforms": [source_list[0].platform] if source_list[0].platform is not None else [],
            "instrument_types": [source_list[0].instrument_type] if source_list[0].instrument_type is not None else [],
            "metadata_filters": []
            },
        "source2": {
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

    # print(conjunction_params)
    
    search_result = requests.post(API_CONJUNCTION_URL, headers={"accept": "application/json", "Content-Type": "application/json"}, json=conjunction_params)
    if search_result.status_code == 200:
        results = json.loads(search_result.text)
    else:
        print("An API error occurred. Status code " + str(search_result.status_code) + ": " + search_result.text)
        results = -1
    
    return results
"""


class GroundInstrument:
    """
    GroundInstrument(program, platform, instrument_type, metadata_filters)
    
    Represents a ground-based ephemeris source.
    """

    def __init__(self, program=None, platform=None, instrument_type=None, metadata_filters=None):
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
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        self.metadata_filters = metadata_filters


class ConjunctionEvent:
    """
    Represents a single conjunction event.
    """

    def __init__(self, conjunction_type=None, e1_source=None, e2_source=None, start=None, end=None, min_distance=None, max_distance=None):
        self.conjunction_type = conjunction_type,
        self.e1_source = e1_source  # store this as GroundInstrument/SpaceInstrument object?
        self.e2_source = e2_source  # store this as GroundInstrument/SpaceInstrument object?
        
        if type(start) is str:
            self.start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            self.end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        else:
            self.start = start
            self.end = end
            
        self.min_distance = min_distance
        self.max_distance = max_distance
        
    def to_dictionary(self):
        """
        Returns a dictionary representation of the conjunction event
        
        :return: a dictionary representation of the conjunction event
        """
        event = {
            "conjunction_type": self.conjunction_type,
            "e1_source": self.e1_source,
            "e2_source": self.e2_source,
            "start": self.start,
            "end": self.end,
            "min_distance": self.min_distance,
            "max_distance": self.max_distance,
            }
        
        return copy.deepcopy(event)
        
    def __str__(self):
        return str(self.to_dictionary())


class MultiConjunctionEvent:
    """
    Represents a multiple-conjunction event.
    """

    def __init__(self, conjunction_type=None, start=None, end=None, distances=None, sources=None):
        if type(start) is str and type(end) is str:
            self.start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            self.end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        else:
            self.start = start
            self.end = end
            
        self.sources = sources
        self.distances = distances
        self.conjunction_type = conjunction_type

    def to_dictionary(self):
        """
        Returns a dictionary representation of the conjunction event
        
        :return: a dictionary representation of the conjunction event
        """
        dict = {
            "sources": self.sources,
            "distances": self.distances,
            "conjunction_type": self.conjunction_type,
            "start": self.start,
            "end": self.end
            }
        
        return copy.deepcopy(dict)


class ConjunctionSearch:
    """
    A class representing the parameters required for a single conjunction search.
    """

    def __init__(self):
        self.API_CONJUNCTION_URL = "http://api.staging.aurorax.space:8080/api/v1/conjunctions/search"
        
        self.ground_instrument = None
        self.space_instrument = None
        self.start = None
        self.end = None
        self.conjunction_types = ["nbtrace"]
        self.max_distance = 500
        
    def to_dictionary(self):
        """
        Returns a dictionary representation of the conjunction search parameters
        
        :return: a dictionary representation of the conjunction search parameters
        """
        conjunction_parameters = {
            "source1": None if self.ground_instrument is None else {
                "programs": None if self.ground_instrument is None else self.ground_instrument["programs"],
                "platforms": None if self.ground_instrument is None else self.ground_instrument["platforms"],
                "instrument_types": None if self.ground_instrument is None else self.ground_instrument["instrument_types"],
                "metadata_filters": None if self.ground_instrument is None else self.ground_instrument["metadata_filters"]
                },
            "source2": None if self.space_instrument is None else {
                "programs": None if self.space_instrument is None else self.space_instrument["programs"],
                "platforms": None if self.space_instrument is None else self.space_instrument["platforms"],
                "instrument_types": None if self.space_instrument is None else self.space_instrument["instrument_types"],
                "metadata_filters": None if self.space_instrument is None else self.space_instrument["metadata_filters"]
                },
            "start": self.start,
            "end": self.end,
            "conjunction_types": self.conjunction_types,
            "max_distance": self.max_distance,
        }
        
        return copy.deepcopy(conjunction_parameters)
        
    def add_ground(self, programs=None, platforms=None, instrument_types=None, metadata_filters=None):
        """
        Adds parameters for a ground instrument to the conjunction search.
        
        :param programs: a list of strings representing the ground instrument programs to search
        :param platforms: a list of strings representing the ground instrument platforms to search
        :param instrument_types: a list of strings representing the ground instrument instrument types to search 
        :param metadata_filters: a list of dictionaries representing metadata filters for the ground instrument
            in the form {"key": <key>, "operator": <operator>, "value": <value>}
        """
        self.ground_instrument = {
            "programs": None,
            "platforms": None,
            "instrument_types": None,
            "metadata_filters": None,
            "hemisphere": None
            }
        
        if programs is not None:
            self.ground_instrument["programs"] = programs

        if platforms is not None:
            self.ground_instrument["platforms"] = platforms

        if instrument_types is not None:
            self.ground_instrument["instrument_types"] = instrument_types

        if metadata_filters is not None:
            self.ground_instrument["metadata_filters"] = metadata_filters
        
    def add_space(self, programs=None, platforms=None, instrument_types=None, metadata_filters=None):
        """
        Adds parameters for a space instrument to the conjunction search.
        
        :param programs: a list of strings representing the space instrument programs to search
        :param platforms: a list of strings representing the space instrument platforms to search
        :param instrument_types: a list of strings representing the space instrument instrument types to search 
        :param metadata_filters: a list of dictionaries representing metadata filters for the space instrument
            in the form {"key": <key>, "operator": <operator>, "value": <value>}
        :param hemisphere: "northern" or "southern"
        """
        self.space_instrument = {
            "programs": None,
            "platforms": None,
            "instrument_types": None,
            "metadata_filters": None,
            "hemisphere": None
            }
        
        if programs is not None:
            self.space_instrument["programs"] = programs

        if platforms is not None:
            self.space_instrument["platforms"] = platforms

        if instrument_types is not None:
            self.space_instrument["instrument_types"] = instrument_types

        if metadata_filters is not None:
            self.space_instrument["metadata_filters"] = metadata_filters
        
    def execute(self):
        """
        Executes the conjunction search and returns the result.
        
        :return: a list of ConjunctionEvent objects, an empty list in case of no results, or -1 in case of error
        """
        dict = copy.deepcopy(self.to_dictionary())
        dict["start"] = dict["start"].strftime("%Y-%m-%dT%H:%M:%S")
        dict["end"] = dict["end"].strftime("%Y-%m-%dT%H:%M:%S")
        
        # remove all keys with None values
        for key in list(dict.keys()):
            if dict[key] is None:
                dict.pop(key)
            elif key == "source1" or key == "source2":
                for source_key in list(dict[key].keys()):
                    if dict[key][source_key] is None:
                        dict[key].pop(source_key)
                        
        search_result = requests.post(self.API_CONJUNCTION_URL, headers={"accept": "application/json", "Content-Type": "application/json"}, json=dict)
        
        if search_result.status_code == 200:
            results_dict = json.loads(search_result.text)["events"]
            print(str(len(results_dict)) + " conjunction events found")
            
            self.results = []
            
            for r in results_dict:
                self.results.append(ConjunctionEvent(**r))
                
        else:
            print("An API error occurred. Try again.")
            print(search_result.text)
            self.results = -1
            
        return self.results


class MultiConjunctionSearch:
    """
    A class representing the parameters required for a multi-conjunction search.
    """

    def __init__(self, start=None, end=None, ground_instruments=None, space_instruments=None, conjunction_types=None, max_distances=None):
        self.API_MULTI_CONJUNCTION_URL = "http://api.staging.aurorax.space:8080/api/v1/conjunctions/search-multi"
        
        self.ground_instruments = [] if ground_instruments is None else ground_instruments
        self.space_instruments = [] if space_instruments is None else space_instruments
        self.start = start
        self.end = end
        self.conjunction_types = ["nbtrace"] if conjunction_types is None else conjunction_types
        self.max_distances = {} if max_distances is None else max_distances
    
    def add_ground(self, programs=None, platforms=None, instrument_types=None, metadata_filters=None):
        """
        Adds parameters for a ground instrument to the conjunction search.
        
        :param programs: a list of strings representing the ground instrument programs to search
        :param platforms: a list of strings representing the ground instrument platforms to search
        :param instrument_types: a list of strings representing the ground instrument instrument types to search 
        :param metadata_filters: a list of dictionaries representing metadata filters for the ground instrument
            in the form {"key": <key>, "operator": <operator>, "value": <value>}
        """
        instrument = {
            "programs": None,
            "platforms": None,
            "instrument_types": None,
            "metadata_filters": None,
            }
        
        if programs is not None:
            instrument["programs"] = programs
        if platforms is not None:
            instrument["platforms"] = platforms
        if instrument_types is not None:
            instrument["instrument_types"] = instrument_types
        if metadata_filters is not None:
            instrument["metadata_filters"] = metadata_filters
    
        self.ground_instruments.append(copy.deepcopy(instrument))
    
    def add_space(self, programs=None, platforms=None, instrument_types=None, metadata_filters=None, hemisphere=None):
        """
        Adds parameters for a space instrument to the conjunction search.
        
        :param programs: a list of strings representing the space instrument programs to search
        :param platforms: a list of strings representing the space instrument platforms to search
        :param instrument_types: a list of strings representing the space instrument instrument types to search 
        :param metadata_filters: a list of dictionaries representing metadata filters for the space instrument
            in the form {"key": <key>, "operator": <operator>, "value": <value>}
        :param hemisphere: "northern" or "southern"
        """
        instrument = {
            "programs": None,
            "platforms": None,
            "instrument_types": None,
            "metadata_filters": None,
            "hemisphere": None
            }
        
        if programs is not None:
            instrument["programs"] = programs
        if platforms is not None:
            instrument["platforms"] = platforms
        if instrument_types is not None:
            instrument["instrument_types"] = instrument_types
        if metadata_filters is not None:
            instrument["metadata_filters"] = metadata_filters
    
        self.space_instruments.append(copy.deepcopy(instrument))
    
    def set_max_distance(self, instrument1, instrument2, distance):
        """
        Sets the maximum distance between two instruments in this multi-conjunction search.
        
        :param instrument1: "ground<list_number>" or "space<list_number>" representing the space/ground isntrument's
        position in the ground_instruments or space_instruments list, e.g. "ground1"
        :param instrument2: "ground<list_number>" or "space<list_number>" representing the space/ground isntrument's
            position in the ground_instruments or space_instruments list, e.g. "space1"
        :param distance: a positive numeric value representing the maximum distance in kilometers between
            instrument1 and instrument2
        """
        if not distance.isnum():
            print("Distance must be a positive integer or float. Try again.")
            return -1
        
        self.max_distances[instrument1 + "-" + instrument2] = distance
    
    def set_all_max_distances(self, distance=500):
        """
        Sets the maximum distance between all pairs of instruments whose maximum distance has not been explicitly
        set using set_max_distance.
        
        :param distance: a positive numeric value representing the maximum distance between instruments
        """
        ground_len = len(self.ground_instruments)
        space_len = len(self.space_instruments)
        
        for ground_index in range(1, ground_len + 1):
            for space_index in range(1, space_len + 1):
                key = "ground" + str(ground_index) + "-space" + str(space_index)
                if key not in self.max_distances:
                    self.max_distances[key] = distance
                    
        for space_index1 in range(1, ground_len):
            for space_index2 in range(1, space_index1):
                key = "space" + str(space_index1) + "-space" + str(space_index2)
                if key not in self.max_distances:
                    self.max_distances[key] = distance
        
        print(self.max_distances)
        
    def to_dictionary(self):
        """
        Returns a dictionary representation of the multi-conjunction search parameters
        
        :return: a dictionary representation of the multi-conjunction search parameters
        """
        dict = {
            "ground": self.ground_instruments,
            "space": self.space_instruments,
            "start": self.start,
            "end": self.end,
            "conjunction_types": self.conjunction_types,
            "max_distances": self.max_distances
            }
        
        return copy.deepcopy(dict)
    
    def execute(self):
        """
        Executes the multi-conjunction search and returns the result.
        
        :return: a list of MultiConjunctionEvent objects, an empty list in case of no results, or -1 in case of error
        """
        dict = copy.deepcopy(self.to_dictionary())
        dict["start"] = dict["start"].strftime("%Y-%m-%dT%H:%M:%S")
        dict["end"] = dict["end"].strftime("%Y-%m-%dT%H:%M:%S")
        
        # remove all keys with None values
        for key in list(dict.keys()):
            if dict[key] is None:
                dict.pop(key)
            elif key == "ground" or key == "space":
                for inst in dict[key]:  # index is a dictionary
                    for source_key in list(inst.keys()):
                        if inst[source_key] is None:
                            inst.pop(source_key)
                        
        search_result = requests.post(self.API_MULTI_CONJUNCTION_URL, headers={"accept": "application/json", "Content-Type": "application/json"}, json=dict)
        if search_result.status_code == 200:
            results_dict = json.loads(search_result.text)["conjunctions"]
            
            self.results = []
            
            for r in results_dict:
                self.results.append(MultiConjunctionEvent(**r))
                
        else:
            print("An API error occurred. Try again.")
            print(search_result.text)
            self.results = -1
            
        return self.results

