Version 1.15.0
-------------------
- updates for serialization of data when `response_format` parameter is used for conjunction/ephemeris/data product searching
- default changed to `True` for the `create_response_format_template()` helper functions
- example notebooks for conjunction/ephemeris/data product updated to include example of using the response format parameter


Version 1.14.0
-------------------
- added support for NumPy 2.0+
- updated dependency ranges to add more flexibility


Version 1.13.0
-------------------
- major updates to test suite
- bugfixes
  - issue when changing matplotlib theme back to 'default'
  - CLI `sources get --format` bugfix for full record format
  - improve handling of conjunction/ephemeris/data product searches that return no results when retrieving data
  - improve handling of conjunction/ephemeris/data product searches which receive incorrect criteria blocks
  - issue when ordering by 'owner' for `aurorax.search.sources.list()` and `aurorax.search.sources.search()` functions
  - incorrect typing for `aurorax.search.data_products.search()` function's `data_product_type` parameter (corrected to be list of literals, instead of single literal)
- removed `aurorax-cli search sources get_stats` command (`aurorax-cli search sources get --include-stats` flag covers this functionality)
- removed `aurorax-cli search util ground_to_nbtrace` and `aurorax-cli search util ground_to_sbtrace` commands (use library functions instead)
- removed setter class for `api_headers` and `srs_obj` in `PyAurorax()` objects
- changed the `distance` parameter for `aurorax.search.conjunctions.create_advanced_distance_combos()` function to be optional, defaulting to None
- added the `aurorax.search.conjunctions.create_response_format_template()` function to assist with specifying the `response_format` parameter to a conjunction search
- changed `aurorax.search.conjunctions.swarmaurora.open_in_browser()` function to raise a ValueError instead of a AuroraXError when the 'browser' parameter was an unsupport choice
- changed `MetadataFilter` and `MetadataFilterExpression` classes to raise ValueError instead of AuroraXError when an unsupported operator was specified
- bump PyUCalgarySRS dependency to latest


Version 1.12.0
-------------------
- updates to conjunction, ephemeris, and data product searching in the `aurorax.search` module
  - added support for custom lat/lon searching (#81)
  - added new criteria block classes to help with searching: `GroundCriteriaBlock`, `SpaceCriteriaBlock`, `EventCriteriaBlock`, and `CustomLocationsCriteriaBlock` (#54, #51)
  - added new `MetadataFilter` and `MetadataFilterExpression` classes to help with searching (#28)
  - removed `epoch_search_precision` field for conjunction searching
  - added `describe()` function to all search objects
  - added ability to do conjunction searches using a dictionary or string, updated examples notebook (#76)
- added `limit` parameter to `aurorax.search.sources.list_in_table()` function
- added `aurorax.search.conjunctions.create_advanced_distance_combos()` helper function for complex conjunction searches
- updates to crib sheets to show how to use updated conjunction, ephemeris, and data products search functions
- type hinting updates
- bump PyUCalgarySRS dependency to latest


Version 1.11.0
-------------------
- updates to docstrings
- added `title` parameter to montage `create()` function
- bump PyUCalgarySRS dependency to latest


Version 1.10.0
-------------------
- refactor `tools` modules to be integrated with `PyAuroraX()` object
- added `progress_bar_backend` parameter to `PyAuroraX()` object
- bump PyUCalgarySRS dependency to latest


Version 1.9.0
-------------------
- bump PyUCalgarySRS dependency to latest


Version 1.8.0
-------------------
- bump PyUCalgarySRS dependency to latest
- added `pretty_print()` functions to all `at.tools` classes
- added level filtering for dataset listing functions


Version 1.7.0
-------------------
- added `pretty_print()` functions to several classes: `DataSource`, `DataSourceStatistics`, `ConjunctionSearch`, `DataProductSearch`, `EphemerisSearch`


Version 1.6.0
-------------------
- added dataset_name optional parameter to the `purge_download_output_root_path()` function


Version 1.5.0
-------------------
- added support for downloading, reading, and analysis of the TREx Spectrograph data
- added support for `start_time` and `end_time` parameters to all read functions
- added `get_dataset()` function for retrieving a specific single dataset


Version 1.4.0
-------------------
- updates for filtering datasets specifically supported by this library


Version 1.3.3
-------------------
- pinned PyUCalgarySRS dependency


Version 1.3.2
--------------------
- bugfix to `scale_intensity()` function to handle scaling a single RGB image


Version 1.3.1
--------------------
- increase PyUCalgarySRS dependency version


Version 1.3.0
--------------------
- adjustment to ATM `forward()` function `timescale_transport` default value. Changed from 5 minutes to 10 minutes.


Version 1.2.0
--------------------
- addition of `prep_grid_image()` function for turning grid data to RGBA for plotting
- added examples for plotting various gridded data


Version 1.1.0
--------------------
- increase PyUCalgarySRS dependency version to support new grid file datasets


Version 1.0.2
--------------------
- bugfix for search engine `get_data` calls where an extra slash in the URL was causing errors


Version 1.0.1
--------------------
- bugfix for TREx RGB mosaic scaling
- added ATM inverse `atmospheric_attenuation_correction` flag
- forced PyUCalgarySRS version 1.0.8 or higher to support the above two fixes


Version 1.0.0
--------------------
Please note that this release contains major breaking changes.

- Major codebase refactor. All functions are now accessed via a PyAuroraX object which must be instantiated. This was done in support of the new submodules.
- Addition of submodules: 
  - `data` for data downloading and reading
  - `models` for using the TREx Auroral Transport Model (ATM)
  - `tools` for All-sky Imager analysis support tools
- Naming convention for exceptions changed. AuroraXException is now AuroraXError ('Exception' changed to 'Error'), adhering to best practices for naming Python exceptions.
- Removed `sources.get_stats()` function. This was deprecated within the AuroraX API, and replaced by `include_stats` flags part of the other data source listing/get functions.
functionality.
- API `authenticate()` function removed. Not necessary anymore due to the refactor.
- Class renames
    - `Ephemeris` renamed to `EphemerisData`
    - `DataProduct` renamed to `DataProductData`
    - Ephemeris `Search` renamed to `EphemerisSearch`
    - Conjunction `Search` renamed to `ConjunctionSearch`
    - Data product `Search` renamed to `DataProductSearch`
- CLI commands previously available are now wrapped into a `search` top level command (ie. `aurorax-cli sources list` is now `aurorax-cli search sources list`)
- Other
  - Add chunking of ephemeris data upload (#80)
  - Collapse data source partial_update function into single update function (#33)
  - Add exception handling for when API is in maintenance mode (#77)
  - Add ability to upload ephemeris records with null location data (#78)
  - Updates to adding data sources (#79)


Version 0.13.3
--------------------
Bugfix for `pyaurorax.Location` class validator


Version 0.13.2
--------------------
Updated data source retrieval to handle new adhoc sources


Version 0.13.1
--------------------
Minor bugfix for Ephemeris class output string


Version 0.13.0
--------------------
Additional error handling for search requests.


Version 0.12.0
--------------------
- Add search request listing to CLI program (#65)
- Remove search_async functions (#49)
- Remove data sources 'partial_update' function (#64)
- Add support for Python 3.10 (#40)


Version 0.11.0
--------------------
Dropped support for Python 3.6 and added support for Python 3.10. Updated various dependency versions.


Version 0.10.0
--------------------
- Add functions for interacting with Swarm-Aurora using conjunction searches (#73)
- Remove default conjunction types of only nbtrace (#72)
- Add functions for getting the request URL (#74)


Version 0.9.0
--------------------
- Final updates for 0.9.0 release (#69)
- Switch data products delete and delete_daterange functions (#68)
- Add aurorax-cli command line application (#30)
- Stack trace when requesting status for a request ID that doesn't exist bug (#67)
- Add error handling for missing data file in get_data requests function (#66)
- Add data source search function (#62)
- More updates for v0.9.0 release (#61)
- Update Jupyter notebooks and standalone tests to sync up with latest codebase (#32)
- Change __repr__ methods to be object format instead of pformatted dicts (#60)
- Make printing of data source object respond to the format parameter (#59)
- Majority of updates for v0.9.0 release (#58)
- Add describe utility functions (#27)
- Simplify the data source get functions (#34)
- Add events to the searches as another criteria block (#50)
- Change max_distances to advanced_distances for conjunction search (#55)
- Make advanced_distances not rely on the default distance (#56)
- Add a set of 'data product type' variables (#52)
- Add metadata filter capabilities to conjunction searches invalid (#53)
- Add a set of 'conjunction type' variables (#47)
- Merge search_async into search function (#48)
- Add a set of 'source_type' variables (#46)
- Add a set of 'format' variables (#43)
- Make aacgmv2 an optional dependency (#45)
- Clean up output from mypy tests (#31)
- Add optional type to functions that need it (#29)
- Reorganize codebase to split into more files (#35)
- Change default data source format to "full_record" (#36)
- Change flake8 dependency into a dev dependency (#37)
- Upgrade dependencies for 0.9.0 release (#38)
- Add MacOS and Windows tests to the CI pipeline (#39)


Version 0.8.0 or earlier
--------------------
Active development. Changes not documented.
