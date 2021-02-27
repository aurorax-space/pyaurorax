# endpoint URLs
DEFAULT_URL_BASE = "https://api.aurorax.space"


class URLs:
    __DEFAULT_URL_DATA_SOURCES = "/api/v1/data-sources"
    __DEFAULT_URL_STATS = "/api/v1/stats"
    __DEFAULT_URL_EPHEMERIS_AVAILABILITY = "/api/v1/availability/ephemeris"
    __DEFAULT_URL_DATA_PRODUCTS_AVAILABILITY = "/api/v1/availability/data_products"
    __DEFAULT_URL_EPHEMERIS_UPLOAD = "/api/v1/data-sources/{}/ephemeris"
    __DEFAULT_URL_EPHEMERIS_SEARCH = "/api/v1/ephemeris/search"
    __DEFAULT_URL_EPHEMERIS_REQUEST = "/api/v1/ephemeris/requests/{}"

    def __init__(self, base_url: str = DEFAULT_URL_BASE) -> None:
        self.__base = base_url
        self.__data_sources = self.__DEFAULT_URL_DATA_SOURCES
        self.__stats = self.__DEFAULT_URL_STATS
        self.__ephemeris_availability = self.__DEFAULT_URL_EPHEMERIS_AVAILABILITY
        self.__data_products_availability = self.__DEFAULT_URL_DATA_PRODUCTS_AVAILABILITY
        self.__ephemeris_search = self.__DEFAULT_URL_EPHEMERIS_SEARCH
        self.__ephemeris_upload = self.__DEFAULT_URL_EPHEMERIS_UPLOAD
        self.__ephemeris_request = self.__DEFAULT_URL_EPHEMERIS_REQUEST

    @property
    def base_url(self) -> str:
        return self.__base

    @base_url.setter
    def base_url(self, value: str) -> None:
        self.__base = value

    @property
    def data_sources_url(self) -> str:
        return "%s%s" % (self.__base, self.__data_sources)

    @property
    def stats_url(self) -> str:
        return "%s%s" % (self.__base, self.__stats)

    @property
    def ephemeris_availability_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_availability)

    @property
    def data_products_availability_url(self) -> str:
        return "%s%s" % (self.__base, self.__data_products_availability)

    @property
    def ephemeris_search_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_search)

    @property
    def ephemeris_upload_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_upload)

    @property
    def ephemeris_request_url(self) -> str:
        return "%s%s" % (self.__base, self.__ephemeris_request)
