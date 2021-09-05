# Data Categories

All data in AuroraX is considered metadata as opposed to raw data or summary data. For example, data product records contain URLs that point to the location of say, a keogram. This allows AuroraX to not be the "owner" of any data, but merely a centralized lookup system with links to different research group's data systems. THEMIS ASI keograms could exist at one location (UCalgary data system) while MIRACLE keograms could exist at another (FMI data system).

AuroraX is powered by a database with two core types of data:

1. [ephemeris](#ephemeris)
2. [data products](#data-products)

## Ephemeris

Ephemeris data are 1-minute location records corresponding the times that a ground-based or space-based instrument was operating. One of the defining qualities of AuroraX is that data contained in the database consists of only times that instruments definitively collected data. This allows applications such as the [Conjunction Search](https://aurorax.space/conjunctionSearch/dropdowns) to return more useful query results; ones where theres definitely data that can be further evaluated by researchers.

### Example record

The following is an example of a ground-based ephemeris record. This is a single record from the THEMIS ASI in Gillam, Manitoba, retrieved using the [PyAuroraX](/pyaurorax/overview) library:

```python
{
    "data_source": {
        "identifier": 46,
        "program": "themis-asi",
        "platform": "gillam",
        "instrument_type": "panchromatic ASI",
        "source_type": "ground",
        "display_name": "THEMIS-ASI GILL",
    },
    "epoch": datetime.datetime(2020, 1, 1, 0, 0),
    "location_geo": Location(lat=56.376723, lon=-94.643664),
    "location_gsm": Location(lat=None, lon=None),
    "nbtrace": Location(lat=56.376723, lon=-94.643664),
    "sbtrace": Location(lat=-72.76907128936035, lon=-134.6681254931047),
    "metadata": {
        "calgary_apa_ml_v1": "classified as not APA",
        "calgary_apa_ml_v1_confidence": 100.0,
        "calgary_cloud_ml_v1": "classified as cloudy",
        "calgary_cloud_ml_v1_confidence": 99.94,
        "clausen_ml_oath": "classified as discrete"
    },
}
```

### Data source

All ephemeris records contain details regarding what data source it is associated with. The level of information returned by the API and PyAuroraX library can be controlled using a "data_source_record_format" parameter, with this example showing the default of "basic_info".

```python hl_lines="2-9"
{
    "data_source": {
        "identifier": 46,
        "program": "themis-asi",
        "platform": "gillam",
        "instrument_type": "panchromatic ASI",
        "source_type": "ground",
        "display_name": "THEMIS-ASI GILL",
    },
    "epoch": datetime.datetime(2020, 1, 1, 0, 0),
    "location_geo": Location(lat=56.376723, lon=-94.643664),
    "location_gsm": Location(lat=None, lon=None),
    "nbtrace": Location(lat=56.376723, lon=-94.643664),
    "sbtrace": Location(lat=-72.76907128936035, lon=-134.6681254931047),
    "metadata": {
        "calgary_apa_ml_v1": "classified as not APA",
        "calgary_apa_ml_v1_confidence": 100.0,
        "calgary_cloud_ml_v1": "classified as cloudy",
        "calgary_cloud_ml_v1_confidence": 99.94,
        "clausen_ml_oath": "classified as discrete"
    },
}
```



### B-Trace values

AuroraX tools such as the [Conjunction Search](https://aurorax.space/conjunctionSearch/dropdowns) looks for times when spacecrafts are magnetically conjugate with ground-based instruments. This is done by using the North/South B-Trace values from [SSCWeb](https://sscweb.gsfc.nasa.gov/) and custom generated values for the ground-based instruments. To generate these values for a ground-based instrument, we use the geographic location do one of two different calculations on it:

```python hl_lines="13-14"
{
    "data_source": {
        "identifier": 46,
        "program": "themis-asi",
        "platform": "gillam",
        "instrument_type": "panchromatic ASI",
        "source_type": "ground",
        "display_name": "THEMIS-ASI GILL",
    },
    "epoch": datetime.datetime(2020, 1, 1, 0, 0),
    "location_geo": Location(lat=56.376723, lon=-94.643664),
    "location_gsm": Location(lat=None, lon=None),
    "nbtrace": Location(lat=56.376723, lon=-94.643664),
    "sbtrace": Location(lat=-72.76907128936035, lon=-134.6681254931047),
    "metadata": {
        "calgary_apa_ml_v1": "classified as not APA",
        "calgary_apa_ml_v1_confidence": 100.0,
        "calgary_cloud_ml_v1": "classified as cloudy",
        "calgary_cloud_ml_v1_confidence": 99.94,
        "clausen_ml_oath": "classified as discrete"
    },
}
```

North B-Trace:

1. If the geographic latitude is &ge; 0, the North B-Trace lat/lon equals the  geographic lat/lon (above is an example of this).
2. If the geographic latitude is &lt; 0, the geographic position is converted to magnetic coordinates, the latitude is set to be positive, and is converted back to geographic coordinates. These new geographic coordinates are used as the North B-Trace.

South B-Trace:

1. If the geographic latitude is &ge; 0, the geographic position is converted to magnetic coordinates, the latitude is set to be negative, and is converted back to geographic coordinates. These new geographic coordinates are used as the South B-Trace.
2. If the geographic latitude is &lt; 0, the South B-Trace lat/lon equals the  geographic lat/lon.

### Metadata

All ephemeris records also have an additional "metadata" field that can contain any further values specific to that 1-min timestamp. This structure is flexible and has no restrictions. Further, these fields can be marked as "searchable" or not using the metadata schema for the given data source. This "searchable" field is purely a flag for the Conjunction Search web UI to say whether it is visible to the user as a choosable filter. It is still technically searchable using the API and PyAuroraX. 

```python hl_lines="15-21"
{
    "data_source": {
        "identifier": 46,
        "program": "themis-asi",
        "platform": "gillam",
        "instrument_type": "panchromatic ASI",
        "source_type": "ground",
        "display_name": "THEMIS-ASI GILL",
    },
    "epoch": datetime.datetime(2020, 1, 1, 0, 0),
    "location_geo": Location(lat=56.376723, lon=-94.643664),
    "location_gsm": Location(lat=None, lon=None),
    "nbtrace": Location(lat=56.376723, lon=-94.643664),
    "sbtrace": Location(lat=-72.76907128936035, lon=-134.6681254931047),
    "metadata": {
        "calgary_apa_ml_v1": "classified as not APA",
        "calgary_apa_ml_v1_confidence": 100.0,
        "calgary_cloud_ml_v1": "classified as cloudy",
        "calgary_cloud_ml_v1_confidence": 99.94,
        "clausen_ml_oath": "classified as discrete"
    },
}
```

In this example, there exists several metadata fields all representing classifications from different machine learning models.

### GSM locations

Please note that GSM data is only available for space-based instruments. This is why the "location_gsm" values are `None`.

```python hl_lines="12"
{
    "data_source": {
        "identifier": 46,
        "program": "themis-asi",
        "platform": "gillam",
        "instrument_type": "panchromatic ASI",
        "source_type": "ground",
        "display_name": "THEMIS-ASI GILL",
    },
    "epoch": datetime.datetime(2020, 1, 1, 0, 0),
    "location_geo": Location(lat=56.376723, lon=-94.643664),
    "location_gsm": Location(lat=None, lon=None),
    "nbtrace": Location(lat=56.376723, lon=-94.643664),
    "sbtrace": Location(lat=-72.76907128936035, lon=-134.6681254931047),
    "metadata": {
        "calgary_apa_ml_v1": "classified as not APA",
        "calgary_apa_ml_v1_confidence": 100.0,
        "calgary_cloud_ml_v1": "classified as cloudy",
        "calgary_cloud_ml_v1_confidence": 99.94,
        "clausen_ml_oath": "classified as discrete"
    },
}
```

## Data Products

In addition to ephemeris metadata, AuroraX also contains metadata representing data products. There are several different types currently: keogram, montage, average, movie, summary_plot, data_availability, and gridded_data.

Keograms are the most recognizable data product for ground-based ASIs; they are images that represent a period of time for imaging. More information about them can be found [here](/about_the_data/instruments/ground/asis/#keograms).

<figure>
  <img src="https://data.swarm-aurora.com/data/summary_data/2008/20080904/themis-asi/20080904_07_gill_themis19_full-keogram.pgm.jpg" />
  <figcaption>THEMIS ASI hourly keogram from Gillam, MB, representing the hour 2008-09-04 UT07</figcaption>
</figure>

AuroraX contains data product records for an assortment of different keograms and are used by web applications such as [Keogramist](https://aurorax.space/keogramist). Below is an example of a daily keogram record in AuroraX:

```python
{
    "data_source": {
        "identifier": 103,
        "program": "trex",
        "platform": "gillam",
        "instrument_type": "RGB ASI",
        "source_type": "ground"
        "display_name": "TREx RGB GILL",
    },
    "data_product_type": "keogram",
    "start": datetime.datetime(2020, 1, 1, 0, 0),
    "end": datetime.datetime(2020, 1, 1, 23, 59),
    "url": "https://data.phys.ucalgary.ca/sort_by_project/TREx/RGB/stream2/2020/01/01/gill_rgb-04/20200101__gill_rgb-04_full-keogram.jpg"
    "metadata": {
        "imaging_end_time": "2020-01-01T13:16:00.000000",
        "imaging_start_time": "2019-12-31T23:30:00.000000",
        "keogram_type": "daily"
    },
}
```

### Data Source

Identical to the ephemeris records, each data product record contains the information about the data source that it is associated with. The level of information returned by the API and PyAuroraX library can be controlled using a "data_source_record_format" parameter, with this example showing the default of "basic_info".

```python hl_lines="2-9"
{
    "data_source": {
        "identifier": 103,
        "program": "trex",
        "platform": "gillam",
        "instrument_type": "RGB ASI",
        "source_type": "ground"
        "display_name": "TREx RGB GILL",
    },
    "data_product_type": "keogram",
    "start": datetime.datetime(2020, 1, 1, 0, 0),
    "end": datetime.datetime(2020, 1, 1, 23, 59),
    "url": "https://data.phys.ucalgary.ca/sort_by_project/TREx/RGB/stream2/2020/01/01/gill_rgb-04/20200101__gill_rgb-04_full-keogram.jpg"
    "metadata": {
        "imaging_end_time": "2020-01-01T13:16:00.000000",
        "imaging_start_time": "2019-12-31T23:30:00.000000",
        "keogram_type": "daily"
    },
}
```

### Data Product Type

As mentioned, there exist several different data product types. These types can be used to filter on when doing data product searches; for example, searching AuroraX for all keograms from the Fort Smith THEMIS ASI on a specific day.

```python hl_lines="10"
{
    "data_source": {
        "identifier": 103,
        "program": "trex",
        "platform": "gillam",
        "instrument_type": "RGB ASI",
        "source_type": "ground"
        "display_name": "TREx RGB GILL",
    },
    "data_product_type": "keogram",
    "start": datetime.datetime(2020, 1, 1, 0, 0),
    "end": datetime.datetime(2020, 1, 1, 23, 59),
    "url": "https://data.phys.ucalgary.ca/sort_by_project/TREx/RGB/stream2/2020/01/01/gill_rgb-04/20200101__gill_rgb-04_full-keogram.jpg"
    "metadata": {
        "imaging_end_time": "2020-01-01T13:16:00.000000",
        "imaging_start_time": "2019-12-31T23:30:00.000000",
        "keogram_type": "daily"
    },
}
```

### Metadata

Much like the ephemeris records, data product records also have a flexible metadata structure that can contain any number and type of fields.

```python hl_lines="14-18"
{
    "data_source": {
        "identifier": 103,
        "program": "trex",
        "platform": "gillam",
        "instrument_type": "RGB ASI",
        "source_type": "ground"
        "display_name": "TREx RGB GILL",
    },
    "data_product_type": "keogram",
    "start": datetime.datetime(2020, 1, 1, 0, 0),
    "end": datetime.datetime(2020, 1, 1, 23, 59),
    "url": "https://data.phys.ucalgary.ca/sort_by_project/TREx/RGB/stream2/2020/01/01/gill_rgb-04/20200101__gill_rgb-04_full-keogram.jpg"
    "metadata": {
        "imaging_end_time": "2020-01-01T13:16:00.000000",
        "imaging_start_time": "2019-12-31T23:30:00.000000",
        "keogram_type": "daily"
    },
}
```
