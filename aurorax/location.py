class Location():
    """
    Class representing an AuroraX location (ie. geographic coordinates,
    GSM coordinates, northern/southern magnetic footprints)
    """

    def __init__(self, lat: float, lon: float):
        """
        Constructor

        :param lat: latitude
        :type lat: float
        :param lon: longitude
        :type lon: float
        """
        self.lat = lat
        self.lon = lon

    def __str__(self) -> str:
        """String method

        :return: string format
        :rtype: str
        """
        return str(self.__dict__)

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return "%s(lat=%f, lon=%f)" % (self.__class__.__name__, self.lat, self.lon)
