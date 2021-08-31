URLS=[
"aurorax/index.html",
"aurorax/metadata.html",
"aurorax/util.html",
"aurorax/data_products.html",
"aurorax/requests.html",
"aurorax/availability.html",
"aurorax/models.html",
"aurorax/ephemeris.html",
"aurorax/sources.html",
"aurorax/api.html",
"aurorax/conjunctions.html",
"aurorax/exceptions.html"
];
INDEX=[
{
"ref":"aurorax",
"url":0,
"doc":"PyAuroraX package."
},
{
"ref":"aurorax.metadata",
"url":1,
"doc":"AuroraX metadata schemas describe the intended structure of metadata stored in ephemeris and data product records."
},
{
"ref":"aurorax.metadata.validate",
"url":1,
"doc":"Validate the metadata record against a schema. This checks that the key names match and there aren't fewer or more keys than expected. Attributes: schema: list of dictionaries representing the metadata schema to validate against record: metadata record dictionary to validate Returns: True if the metadata record is valid",
"func":1
},
{
"ref":"aurorax.metadata.get_ephemeris_schema",
"url":1,
"doc":"Retrieve the metadata schema for an ephemeris record Attributes: identifier: ephemeris source ID Returns: Metadata schema associated with the record",
"func":1
},
{
"ref":"aurorax.metadata.get_data_products_schema",
"url":1,
"doc":"Retrieve the metadata schema for a data products record Attributes: identifier: ephemeris source ID Returns: Metadata schema associated with the record",
"func":1
},
{
"ref":"aurorax.util",
"url":2,
"doc":"Utility methods for converting geographic locations to North/South B trace coordinates."
},
{
"ref":"aurorax.util.ground_geo_to_nbtrace",
"url":2,
"doc":"Convert geographic location to North B-Trace geographic location. Attributes: geo_location: aurorax.Location object representing the geographic location dt: datetime.datetime object representing the timestamp Returns: North B-trace location as an aurorax.Location object",
"func":1
},
{
"ref":"aurorax.util.ground_geo_to_sbtrace",
"url":2,
"doc":"Convert geographic location to South B-Trace geographic location. Attributes: geo_location: aurorax.Location object representing the geographic location dt: datetime.datetime object representing the timestamp Returns: South B-trace location as an aurorax.Location object",
"func":1
},
{
"ref":"aurorax.data_products",
"url":3,
"doc":"AuroraX holds records for various types of data products produced by ground and space instruments. The most common type of data product is the keogram."
},
{
"ref":"aurorax.data_products.DataProduct",
"url":3,
"doc":"DataProduct data type Attributes: data_source: aurorax.sources.DataSource source that the ephemeris record is associated with data_product_type: data product type (\"keogram\", \"movie\", \"summary_plot\") start: starting datetime.datetime timestamp for the record in UTC end: ending datetime.datetime timestamp for the record in UTC url: URL location string of data product metdata: metadata dictionary for this record Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.data_products.DataProduct.data_source",
"url":3,
"doc":""
},
{
"ref":"aurorax.data_products.DataProduct.data_product_type",
"url":3,
"doc":""
},
{
"ref":"aurorax.data_products.DataProduct.start",
"url":3,
"doc":""
},
{
"ref":"aurorax.data_products.DataProduct.end",
"url":3,
"doc":""
},
{
"ref":"aurorax.data_products.DataProduct.url",
"url":3,
"doc":""
},
{
"ref":"aurorax.data_products.DataProduct.metadata",
"url":3,
"doc":""
},
{
"ref":"aurorax.data_products.DataProduct.to_json_serializable",
"url":3,
"doc":"Convert object to a JSON-serializable object (ie. translate datetime objects to strings) Returns: Dictionary JSON-serializable object",
"func":1
},
{
"ref":"aurorax.data_products.upload",
"url":3,
"doc":"Upload data product records to AuroraX Attributes: identifier: AuroraX data source ID int records: list of aurorax.data_products.DataProduct records to upload validate_source: boolean, set to True to validate all records before uploading Returns: 1 for success, raises exception on error Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error aurorax.exceptions.AuroraXUploadException: upload error aurorax.exceptions.AuroraXValidationException: data source validation error",
"func":1
},
{
"ref":"aurorax.data_products.delete_daterange",
"url":3,
"doc":"Deletes data products associated with a data source in the date range provided. This method is asynchronous. Attributes: data_source: aurorax.sources.DataSource source associated with the data product records. Identifier, program, platform, and instrument_type are required. start: datetime.datetime beginning of range to delete records for, inclusive. end: datetime.datetime end of datetime range to delete records for, inclusive. data_product_types: specific types of data product to delete, e.g. [\"keogram\", \"movie\"]. If omitted, all data product types will be deleted. Returns: 1 on success Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXNotFoundException: source not found aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.data_products.delete",
"url":3,
"doc":"Delete data products by URL. This method is asynchronous. Attributes: data_source: aurorax.sources.DataSource source associated with the data product records. Identifier, program, platform, and instrument_type are required. urls: list of URL strings associated with the data products being deleted Returns: 1 on success Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXNotFoundException: source not found aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.data_products.Search",
"url":3,
"doc":"Class representing an AuroraX data products search start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search programs: list of program names to search platforms: list of platform names to search instrument_types: list of instrument types to search metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } data_product_type_filters: list of dictionaries describing data product types to filter on e.g. \"keogram\", defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } request: aurorax.AuroraXResponse object returned when the search is executed request_id: unique AuroraX string ID assigned to the request request_url: unique AuroraX URL string assigned to the request executed: boolean, gets set to True when the search is executed completed: boolean, gets set to True when the search is checked to be finished data_url: URL string where data is accessed query: dictionary of values sent for the search query status: dictionary of status updates data: list of aurorax.data_products.DataProduct objects returned logs: list of logging messages from the API Create a new Search object"
},
{
"ref":"aurorax.data_products.Search.execute",
"url":3,
"doc":"Initiate data products search request",
"func":1
},
{
"ref":"aurorax.data_products.Search.update_status",
"url":3,
"doc":"Update the status of this data products search request Attributes: status: retrieved status dictionary (include to avoid requesting it from the API again), defaults to None",
"func":1
},
{
"ref":"aurorax.data_products.Search.check_for_data",
"url":3,
"doc":"Check to see if data is available for this data products search request",
"func":1
},
{
"ref":"aurorax.data_products.Search.get_data",
"url":3,
"doc":"Retrieve the data available for this data products search request",
"func":1
},
{
"ref":"aurorax.data_products.Search.wait",
"url":3,
"doc":"Block and wait for the request to complete and data is available for retrieval Attributes: poll_interval: time in seconds to wait between polling attempts, defaults to aurorax.requests.STANDARD_POLLING_SLEEP_TIME verbose: output poll times, defaults to False",
"func":1
},
{
"ref":"aurorax.data_products.Search.cancel",
"url":3,
"doc":"Cancel the data product search request at the API. This method returns asynchronously by default. Attributes: wait: set to True to block until the cancellation request has been completed. This may take several minutes. verbose: when wait=True, output poll times, defaults to False poll_interval: when wait=True, seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME Returns: 1 on success Raises: aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.data_products.search_async",
"url":3,
"doc":"Submit a request for a data products search, return asynchronously. Attributes: start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search programs: list of programs to search through, defaults to None platforms: list of platforms to search through, defaults to None instrument_types: list of instrument types to search through, defaults to None metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } data_product_type_filters: list of dictionaries describing data product types to filter on e.g. \"keogram\", defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } Returns: aurorax.data_products.Search object",
"func":1
},
{
"ref":"aurorax.data_products.search",
"url":3,
"doc":"Search for data product records and block until results are returned. Attributes: start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search programs: list of programs to search through, defaults to None platforms: list of platforms to search through, defaults to None instrument_types: list of instrument types to search through, defaults to None metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } data_product_type_filters: list of dictionaries describing data product types to filter on e.g. \"keogram\", defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } verbose: output poll times, defaults to False poll_interval: time in seconds to wait between polling attempts, defaults to aurorax.requests.STANDARD_POLLING_SLEEP_TIME Returns: aurorax.data_products.Search object",
"func":1
},
{
"ref":"aurorax.requests",
"url":4,
"doc":"The requests module contains methods for retrieving data from an AuroraX request."
},
{
"ref":"aurorax.requests.get_status",
"url":4,
"doc":"Retrieve the status of a request Attributes: request_url: URL of the request information Returns: Status dictionary for the request",
"func":1
},
{
"ref":"aurorax.requests.get_data",
"url":4,
"doc":"Retrieve the data for a request Attributes: data_url: URL for the data of a request Returns: List of JSON data objects in the response",
"func":1
},
{
"ref":"aurorax.requests.get_logs",
"url":4,
"doc":"Retrieve the logs for a request Attributes: request_url: URL of the request information Returns: List of logged messages for the request",
"func":1
},
{
"ref":"aurorax.requests.wait_for_data",
"url":4,
"doc":"Block and wait for the data to be made available for a request Attributes: request_url: URL of the request information poll_interval: seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME verbose: output poll times, defaults to False Returns: Status dictionary for the request",
"func":1
},
{
"ref":"aurorax.requests.cancel",
"url":4,
"doc":"Cancel the request at the given URL. This operation is asynchronous by default unless the wait param is set to True. Attributes: request_url: URL string of the request to be canceled wait: set to True to block until the cancellation request has been completed. This may take several minutes. verbose: when wait=True, output poll times, defaults to False poll_interval: when wait=True, seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME Returns: 1 on success Raises: aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.availability",
"url":5,
"doc":"The availability module provides the means to quickly determine the availability of desired ephemeris or data product records in AuroraX."
},
{
"ref":"aurorax.availability.AvailabilityResult",
"url":5,
"doc":"Availability result data type. Attributes: data_source: aurorax.sources.DataSource object that the ephemeris record is associated with available_data_products: data product availability dictionary of shape {\"YYYY-MM-DD\":  } available_ephemeris: ephemeris availability dictionary of shape {\"YYYY-MM-DD\":  } Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.availability.AvailabilityResult.data_source",
"url":5,
"doc":""
},
{
"ref":"aurorax.availability.AvailabilityResult.available_data_products",
"url":5,
"doc":""
},
{
"ref":"aurorax.availability.AvailabilityResult.available_ephemeris",
"url":5,
"doc":""
},
{
"ref":"aurorax.availability.ephemeris",
"url":5,
"doc":"Retrieve information about the number of existing ephemeris records. Attributes: start: start datetime.date end: end datetime.date program: program string name to filter sources by, defaults to None platform: platform string name to filter sources by, defaults to None instrument_type: instrument type string to filter sources by, defaults to None source_type: source type string to filter sources by (heo, leo, lunar, or ground), defaults to None owner: owner email address string to filter sources by, defaults to None format: the format of the data sources returned (identifier_only, basic_info, full_record), defaults to \"basic_info\" Returns: A list of aurorax.availability.AvailabilityResult objects",
"func":1
},
{
"ref":"aurorax.availability.data_products",
"url":5,
"doc":"Retrieve information about the number of existing data product records Attributes: start: start datetime.date end: end datetime.date program: program string name to filter sources by, defaults to None platform: platform string name to filter sources by, defaults to None instrument_type: instrument type string to filter sources by, defaults to None source_type: source type string to filter sources by (heo, leo, lunar, or ground), defaults to None owner: owner email address string to filter sources by, defaults to None format: the format of the data sources returned (identifier_only, basic_info, full_record), defaults to \"basic_info\" Returns: A list of aurorax.availability.AvailabilityResult objects",
"func":1
},
{
"ref":"aurorax.models",
"url":6,
"doc":"This module contains the Location class."
},
{
"ref":"aurorax.models.Location",
"url":6,
"doc":"Class representing an AuroraX location (ie. geographic coordinates, GSM coordinates, northern/southern magnetic footprints) Attributes: lat: latitude lon: longitude Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.models.Location.lat",
"url":6,
"doc":""
},
{
"ref":"aurorax.models.Location.lon",
"url":6,
"doc":""
},
{
"ref":"aurorax.models.Location.both_must_be_none_or_number",
"url":6,
"doc":"",
"func":1
},
{
"ref":"aurorax.ephemeris",
"url":7,
"doc":"AuroraX holds ephemeris records for ground and space instruments in operation."
},
{
"ref":"aurorax.ephemeris.Ephemeris",
"url":7,
"doc":"Ephemeris data type Attributes: data_source: aurorax.sources.DataSource source that the ephemeris record is associated with epoch: datetime.datetime timestamp for the record in UTC location_geo: aurorax.Location object with latitude and longitude in geographic coordinates location_gsm: aurorax.Location object with latitude and longitude in GSM coordinates (leave empty for data sources with a type of 'ground') nbtrace: aurorax.Location object with north B-trace geomagnetic latitude and longitude sbtrace: aurorax.Location object with south B-trace geomagnetic latitude and longitude metadata: dictionary containing metadata values for this record Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.ephemeris.Ephemeris.data_source",
"url":7,
"doc":""
},
{
"ref":"aurorax.ephemeris.Ephemeris.epoch",
"url":7,
"doc":""
},
{
"ref":"aurorax.ephemeris.Ephemeris.location_geo",
"url":7,
"doc":""
},
{
"ref":"aurorax.ephemeris.Ephemeris.location_gsm",
"url":7,
"doc":""
},
{
"ref":"aurorax.ephemeris.Ephemeris.nbtrace",
"url":7,
"doc":""
},
{
"ref":"aurorax.ephemeris.Ephemeris.sbtrace",
"url":7,
"doc":""
},
{
"ref":"aurorax.ephemeris.Ephemeris.metadata",
"url":7,
"doc":""
},
{
"ref":"aurorax.ephemeris.Ephemeris.to_json_serializable",
"url":7,
"doc":"Convert object to a JSON-serializable object (ie. translate datetime objects to strings) Returns: Dictionary JSON-serializable object",
"func":1
},
{
"ref":"aurorax.ephemeris.Search",
"url":7,
"doc":"Class representing an AuroraX ephemeris search start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search programs: list of program names to search platforms: list of platform names to search instrument_types: list of instrument types to search metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } request: aurorax.AuroraXResponse object returned when the search is executed request_id: unique AuroraX string ID assigned to the request request_url: unique AuroraX URL string assigned to the request executed: boolean, gets set to True when the search is executed completed: boolean, gets set to True when the search is checked to be finished data_url: URL string where data is accessed query: dictionary of values sent for the search query status: dictionary of status updates data: list of aurorax.ephemeris.Ephemeris objects returned logs: list of logging messages from the API Create a new Search object"
},
{
"ref":"aurorax.ephemeris.Search.execute",
"url":7,
"doc":"Initiate ephemeris search request",
"func":1
},
{
"ref":"aurorax.ephemeris.Search.update_status",
"url":7,
"doc":"Update the status of this ephemeris search request Attributes: status: retrieved status dictionary (include to avoid requesting it from the API again), defaults to None",
"func":1
},
{
"ref":"aurorax.ephemeris.Search.check_for_data",
"url":7,
"doc":"Check to see if data is available for this ephemeris search request",
"func":1
},
{
"ref":"aurorax.ephemeris.Search.get_data",
"url":7,
"doc":"Retrieve the data available for this ephemeris search request",
"func":1
},
{
"ref":"aurorax.ephemeris.Search.wait",
"url":7,
"doc":"Block and wait for the request to complete and data is available for retrieval Attributes: poll_interval: time in seconds to wait between polling attempts, defaults to aurorax.requests.STANDARD_POLLING_SLEEP_TIME verbose: output poll times, defaults to False",
"func":1
},
{
"ref":"aurorax.ephemeris.Search.cancel",
"url":7,
"doc":"Cancel the ephemeris search request at the API. This method returns asynchronously by default. Attributes: wait: set to True to block until the cancellation request has been completed. This may take several minutes. verbose: when wait=True, output poll times, defaults to False poll_interval: when wait=True, seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME Returns: 1 on success Raises: aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.ephemeris.search_async",
"url":7,
"doc":"Submit a request for an ephemeris search, return asynchronously Attributes: start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search programs: list of programs to search through, defaults to None platforms: list of platforms to search through, defaults to None instrument_types: list of instrument types to search through, defaults to None metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } Returns: aurorax.ephemeris.Search object",
"func":1
},
{
"ref":"aurorax.ephemeris.search",
"url":7,
"doc":"Search for ephemeris records Attributes: start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search programs: list of programs to search through, defaults to None platforms: list of platforms to search through, defaults to None instrument_types: list of instrument types to search through, defaults to None metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None. e.g. { \"key\": \"string\", \"operator\": \"=\", \"values\": [ \"string\" ] } verbose: output poll times, defaults to False poll_interval: time in seconds to wait between polling attempts, defaults to aurorax.requests.STANDARD_POLLING_SLEEP_TIME Returns: aurorax.ephemeris.Search object",
"func":1
},
{
"ref":"aurorax.ephemeris.upload",
"url":7,
"doc":"Upload ephemeris records to AuroraX Attributes: identifier: AuroraX data source ID int records: list of aurorax.ephemeris.Ephemeris records to upload validate_source: boolean, set to True to validate all records before uploading Returns: 1 for success, raises exception on error Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error aurorax.exceptions.AuroraXUploadException: upload error aurorax.exceptions.AuroraXValidationException: data source validation error",
"func":1
},
{
"ref":"aurorax.ephemeris.delete",
"url":7,
"doc":"Delete a range of ephemeris records. This method is asynchronous. Attributes: data_source: aurorax.sources.DataSource source associated with the data product records. Identifier, program, platform, and instrument_type are required. start: datetime.datetime beginning of range to delete records for, inclusive. end: datetime.datetime end of datetime range to delete records for, inclusive. Returns: 1 on success Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXNotFoundException: source not found aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.sources",
"url":8,
"doc":"AuroraX data sources are unique instruments that produce ephemeris or data product records."
},
{
"ref":"aurorax.sources.DataSource",
"url":8,
"doc":"Data source data type Attributes: identifier: an integer unique to the data source program: a string representing the data source program platform: a string representing the data source platform instrument_type: a string representing the data source instrument type source_type: a string representing the data source type display_name: a string representing the data source's proper display name metadata: a dictionary of metadata properties owner: a string representing the data source's owner in AuroraX maintainers: a list of strings representing the email addresses of AuroraX accounts that can alter this data source and its associated records ephemeris_metadata_schema: a list of dictionaries capturing the metadata keys and values that can appear in ephemeris records associated with the data source data_product_metadata_schema: a list of dictionaries capturing the metadata keys and values that can appear in data product records associated with the data source Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.sources.DataSource.identifier",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.program",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.platform",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.instrument_type",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.source_type",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.display_name",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.metadata",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.owner",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.maintainers",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.ephemeris_metadata_schema",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.DataSource.data_product_metadata_schema",
"url":8,
"doc":""
},
{
"ref":"aurorax.sources.list",
"url":8,
"doc":"Retrieve all data source records. Attributes: order: string value to order results by (identifier, program, platform, instrument_type, display_name, owner), defaults to \"identifier\" format: string record format, defaults to \"basic_info\" Returns: A list of AuroraX DataSource objects Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error",
"func":1
},
{
"ref":"aurorax.sources.get",
"url":8,
"doc":"Retrieve a specific data source record. Attributes: program: the string name of the program platform: the string name of the platform instrument_type: the string name of the instrument type format: record format, defaults to \"basic_info\" Returns: An AuroraX DataSource object matching the input parameters Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXNotFoundException: source not found",
"func":1
},
{
"ref":"aurorax.sources.get_using_filters",
"url":8,
"doc":"Retrieve all data source records matching a filter. Attributes: program: the string name of the program platform: the string name of the platform instrument_type: the string name of the instrument type source_type: the string name of the data source type owner: the AuroraX data source owner's email address format: record format, defaults to \"basic_info\" order: string value to order results by (identifier, program, platform, instrument_type, display_name, owner), defaults to \"identifier\" Returns: A list of AuroraX DataSource objects matching the filter parameters Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error",
"func":1
},
{
"ref":"aurorax.sources.get_using_identifier",
"url":8,
"doc":"Retrieve data source record matching an identifier. Attributes: identifier: an integer unique to the data source format: record format, defaults to \"basic_info\" Returns: An AuroraX DataSource object matching the input identifier. Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error",
"func":1
},
{
"ref":"aurorax.sources.get_stats",
"url":8,
"doc":"Retrieve statistics for a data source. Attributes: identifier: an integer unique to the data source format: record format, defaults to \"basic_info\" slow: a boolean indicating whether to use slow method which gets most up-to-date stats info Returns: A dictionary of statistics information about the data source. Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error :return: stats info :rtype: Dict",
"func":1
},
{
"ref":"aurorax.sources.add",
"url":8,
"doc":"Add a new data source to AuroraX. Attributes: data_source: the fully defined AuroraX DataSource object to add Returns: The newly created AuroraX DataSource object. Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXDuplicateException: duplicate data source, already exists",
"func":1
},
{
"ref":"aurorax.sources.delete",
"url":8,
"doc":"Delete a data source from AuroraX. Attributes: identifier: an integer unique to the data source Returns: 1 on success. Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXNotFoundException: data source not found aurorax.exceptions.AuroraXConflictException: conflict of some type",
"func":1
},
{
"ref":"aurorax.sources.update",
"url":8,
"doc":"Update a data source in AuroraX. This operation will fully replace the data source with the data_source argument passed in. Please make sure data_source is complete. Refer to examples for usage. Attributes: data_source: the fully defined AuroraX DataSource object to update Returns: The updated AuroraX DataSource object. Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXNotFoundException: data source not found aurorax.exceptions.AuroraXBadParametersException: missing parameters",
"func":1
},
{
"ref":"aurorax.sources.partial_update",
"url":8,
"doc":"Partially update a data source in AuroraX. Omitted fields are ignored in the update. Refer to examples for usage. Attributes: identifier: an integer unique to the data source program: a string representing the data source program platform: a string representing the data source platform instrument_type: a string representing the data source instrument type source_type: a string representing the data source type display_name: a string representing the data source's proper display name metadata: a dictionary of metadata properties owner: a string representing the data source's owner in AuroraX maintainers: a list of strings representing the email addresses of AuroraX accounts that can alter this data source and its associated records ephemeris_metadata_schema: a list of dictionaries capturing the metadata keys and values that can appear in ephemeris records associated with the data source data_product_metadata_schema: a list of dictionaries capturing the metadata keys and values that can appear in data product records associated with the data source Returns: The updated AuroraX DataSource object. Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXNotFoundException: data source not found aurorax.exceptions.AuroraXBadParametersException: missing parameters",
"func":1
},
{
"ref":"aurorax.api",
"url":9,
"doc":"The API module contains classes and methods used throughout PyAuroraX for API interaction."
},
{
"ref":"aurorax.api.get_api_key",
"url":9,
"doc":"",
"func":1
},
{
"ref":"aurorax.api.authenticate",
"url":9,
"doc":"Set authentication values for use with subsequent queries Attributes: api_key: AuroraX API key string Returns: 0",
"func":1
},
{
"ref":"aurorax.api.AuroraXResponse",
"url":9,
"doc":"Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.api.AuroraXResponse.request",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXResponse.data",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXResponse.status_code",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXRequest",
"url":9,
"doc":"Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.api.AuroraXRequest.url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXRequest.method",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXRequest.params",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXRequest.body",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXRequest.headers",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXRequest.null_response",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.AuroraXRequest.execute",
"url":9,
"doc":"Execute an AuroraX request Attributes: limited_evaluation: set this to True if you don't want to evaluate the response outside of the retry mechanism, defaults to False Returns: An AuroraXResponse object Raises: aurorax.exceptions.AuroraXMaxRetriesException: max retry error aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.api.URLs",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.base_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.data_sources_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.stats_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.ephemeris_availability_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.data_products_availability_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.ephemeris_search_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.ephemeris_upload_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.ephemeris_request_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.data_products_search_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.data_products_upload_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.data_products_request_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.conjunction_search_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.URLs.conjunction_request_url",
"url":9,
"doc":""
},
{
"ref":"aurorax.api.set_base_url",
"url":9,
"doc":"Change the base URL for the API (ie. change to the staging system or local server) Attributes: url: new base url string (ie. 'https: api.staging.aurorax.space')",
"func":1
},
{
"ref":"aurorax.api.reset_base_url",
"url":9,
"doc":"Set the base URL for the API back to the default",
"func":1
},
{
"ref":"aurorax.conjunctions",
"url":10,
"doc":"AuroraX provides a conjunction module for finding conjunction events between ground and space instruments, and between space instruments."
},
{
"ref":"aurorax.conjunctions.Conjunction",
"url":10,
"doc":"Conjunction data type. Attributes: conjunction_type: conjunction type \"nbtrace\" or \"sbtrace\" start: start datetime.datetime of conjunction event(s) end: end datetime.datetime of conjunction event(s) data_sources: aurorax.sources.DataSource sources in the conjunction min_distance: minimum kilometre distance of conjunction event(s), float max_distance: maximum kilometre distance of conjunction event(s), float events: list of dictionaries containing details of individual conjunction events Create a new model by parsing and validating input data from keyword arguments. Raises ValidationError if the input data cannot be parsed to form a valid model."
},
{
"ref":"aurorax.conjunctions.Conjunction.conjunction_type",
"url":10,
"doc":""
},
{
"ref":"aurorax.conjunctions.Conjunction.start",
"url":10,
"doc":""
},
{
"ref":"aurorax.conjunctions.Conjunction.end",
"url":10,
"doc":""
},
{
"ref":"aurorax.conjunctions.Conjunction.data_sources",
"url":10,
"doc":""
},
{
"ref":"aurorax.conjunctions.Conjunction.min_distance",
"url":10,
"doc":""
},
{
"ref":"aurorax.conjunctions.Conjunction.max_distance",
"url":10,
"doc":""
},
{
"ref":"aurorax.conjunctions.Conjunction.events",
"url":10,
"doc":""
},
{
"ref":"aurorax.conjunctions.Search",
"url":10,
"doc":"Class representing an AuroraX conjunctions search Attributes: start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search ground: List of ground instrument search parameters. See examples for usage. e.g. [ { \"programs\": [\"themis-asi\"], \"platforms\": [\"gillam\", \"rabbit lake\"], \"instrument_types\": [\"RGB\"] } ] space: List of one or more space instrument search parameters. See examples for usage. e.g. [ { \"programs\": [\"themis-asi\", \"swarm\"], \"platforms\": [\"themisa\", \"swarma\"], \"instrument_types\": [\"footprint\"] } ] conjunction_types: list of conjunction types, defaults to [\"nbtrace\"] max_distances: dictionary of Dict[str, float] ground-space and space-space maximum distances for conjunctions. default_distance will be used for any ground-space and space-space maximum distances not specified. See examples for usage. e.g. distances = { \"ground1-ground2\": None, \"ground1-space1\": 500, \"ground1-space2\": 500, \"ground2-space1\": 500, \"ground2-space2\": 500, \"space1-space2\": None } default_distance: default maximum distance in kilometers for conjunction. Used when max distance is not specified for any ground-space and space-space instrument pairs. request: aurorax.AuroraXResponse object returned when the search is executed request_id: unique AuroraX string ID assigned to the request request_url: unique AuroraX URL string assigned to the request executed: boolean, gets set to True when the search is executed completed: boolean, gets set to True when the search is checked to be finished data_url: URL string where data is accessed query: dictionary of values sent for the search query status: dictionary of status updates data: list of aurorax.conjunctions.Conjunction objects returned logs: list of logging messages from the API Returns: aurorax.conjunctions.Search object"
},
{
"ref":"aurorax.conjunctions.Search.execute",
"url":10,
"doc":"Initiate conjunction search request",
"func":1
},
{
"ref":"aurorax.conjunctions.Search.update_status",
"url":10,
"doc":"Update the status of this conjunctions search Attributes: status: retrieved status dictionary (include to avoid requestinf it from the API again), defaults to None",
"func":1
},
{
"ref":"aurorax.conjunctions.Search.check_for_data",
"url":10,
"doc":"Check to see if data is available for this conjunctions search request",
"func":1
},
{
"ref":"aurorax.conjunctions.Search.get_data",
"url":10,
"doc":"",
"func":1
},
{
"ref":"aurorax.conjunctions.Search.wait",
"url":10,
"doc":"Block and wait until the request is complete and data is available for retrieval Attributes: poll_interval: time in seconds to wait between polling attempts, defaults to aurorax.requests.STANDARD_POLLING_SLEEP_TIME verbose: output poll times, defaults to False",
"func":1
},
{
"ref":"aurorax.conjunctions.Search.cancel",
"url":10,
"doc":"Cancel the conjunction search request at the API. This method returns asynchronously by default. Attributes: wait: set to True to block until the cancellation request has been completed. This may take several minutes. verbose: when wait=True, output poll times, defaults to False poll_interval: when wait=True, seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME Returns: 1 on success Raises: aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error aurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation",
"func":1
},
{
"ref":"aurorax.conjunctions.search_async",
"url":10,
"doc":"Submit a request for a conjunctions search, return asynchronously. Attributes: start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search ground: List of ground instrument search parameters. See examples for usage. e.g. [ { \"programs\": [\"themis-asi\"], \"platforms\": [\"gillam\", \"rabbit lake\"], \"instrument_types\": [\"RGB\"] } ] space: List of one or more space instrument search parameters. See examples for usage. e.g. [ { \"programs\": [\"themis-asi\", \"swarm\"], \"platforms\": [\"themisa\", \"swarma\"], \"instrument_types\": [\"footprint\"] } ] conjunction_types: list of conjunction types, defaults to [\"nbtrace\"] max_distances: dictionary of Dict[str, float] ground-space and space-space maximum distances for conjunctions. default_distance will be used for any ground-space and space-space maximum distances not specified. See examples for usage. e.g. distances = { \"ground1-ground2\": None, \"ground1-space1\": 500, \"ground1-space2\": 500, \"ground2-space1\": 500, \"ground2-space2\": 500, \"space1-space2\": None } default_distance: default maximum distance in kilometers for conjunction. Used when max distance is not specified for any ground-space and space-space instrument pairs. Returns: aurorax.conjunctions.Search object",
"func":1
},
{
"ref":"aurorax.conjunctions.search",
"url":10,
"doc":"Search for conjunctions and block until results are returned. Attributes: start: start datetime.datetime timestamp of the search end: end datetime.datetime timestamp of the search ground: List of ground instrument search parameters. See examples for usage. e.g. [ { \"programs\": [\"themis-asi\"], \"platforms\": [\"gillam\", \"rabbit lake\"], \"instrument_types\": [\"RGB\"] } ] space: List of one or more space instrument search parameters. See examples for usage. e.g. [ { \"programs\": [\"themis-asi\", \"swarm\"], \"platforms\": [\"themisa\", \"swarma\"], \"instrument_types\": [\"footprint\"] } ] conjunction_types: list of conjunction types, defaults to [\"nbtrace\"] max_distances: dictionary of Dict[str, float] ground-space and space-space maximum distances for conjunctions. default_distance will be used for any ground-space and space-space maximum distances not specified. See examples for usage. e.g. distances = { \"ground1-ground2\": None, \"ground1-space1\": 500, \"ground1-space2\": 500, \"ground2-space1\": 500, \"ground2-space2\": 500, \"space1-space2\": None } default_distance: default maximum distance in kilometers for conjunction. Used when max distance is not specified for any ground-space and space-space instrument pairs. verbose: boolean to show the progress of the request using the request log, defaults to False poll_interval: seconds to wait between polling calls, defaults to aurorax.requests.STANDARD_POLLING_SLEEP_TIME Returns: aurorax.conjunctions.Search object",
"func":1
},
{
"ref":"aurorax.exceptions",
"url":11,
"doc":"The exceptions module contains descriptive exceptions unique to AuroraX."
},
{
"ref":"aurorax.exceptions.AuroraXException",
"url":11,
"doc":"Common base class for all non-exit exceptions."
},
{
"ref":"aurorax.exceptions.AuroraXNotFoundException",
"url":11,
"doc":"The AuroraX record was not found."
},
{
"ref":"aurorax.exceptions.AuroraXDuplicateException",
"url":11,
"doc":"A duplicate record already exists."
},
{
"ref":"aurorax.exceptions.AuroraXValidationException",
"url":11,
"doc":"Validation of data failed."
},
{
"ref":"aurorax.exceptions.AuroraXUnexpectedContentTypeException",
"url":11,
"doc":"The API responded with an unexpected content type."
},
{
"ref":"aurorax.exceptions.AuroraXMaxRetriesException",
"url":11,
"doc":"The maximum number of retries for the request has been reached."
},
{
"ref":"aurorax.exceptions.AuroraXBadParametersException",
"url":11,
"doc":"Bad parameters were given in the request."
},
{
"ref":"aurorax.exceptions.AuroraXUnauthorizedException",
"url":11,
"doc":"A privileged operation was attempted without authorization."
},
{
"ref":"aurorax.exceptions.AuroraXConflictException",
"url":11,
"doc":"A conflict occurred while modifying records."
},
{
"ref":"aurorax.exceptions.AuroraXUploadException",
"url":11,
"doc":"Error occurred during upload operation."
}
]