# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Class representation for a mosaic.
"""

import os
import datetime
import warnings
import pyproj
import aacgmv2
import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
import cartopy.feature
import cartopy.crs
from copy import copy
from dataclasses import dataclass
from typing import List, Dict, Tuple, Sequence, Union, Optional, Any
from numpy import ndarray
from matplotlib.collections import PolyCollection
from cartopy.crs import Projection


@dataclass
class MosaicSkymap:
    """
    Prepared skymap data for use by mosaic routines.

    Attributes:
        site_uid_list (List[str]): 
            List of site unique identifiers contained within this object.
        elevation (List[numpy.ndarray]): 
            List of elevation data, with each element corresponding to each site. Order 
            matches that of the `site_uid_list` attribute.
        polyfoll_lat (List[numpy.ndarray]): 
            List of latitude polygon data, with each element corresponding to each site. 
            Order matches that of the `site_uid_list` attribute. 
        polyfoll_lon (List[numpy.ndarray]): 
            List of longitude polygon data, with each element corresponding to each site. 
            Order matches that of the `site_uid_list` attribute. 
    """

    site_uid_list: List[str]
    elevation: List[ndarray]
    polyfill_lat: List[ndarray]
    polyfill_lon: List[ndarray]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        unique_polyfill_lat_dims = str(list(dict.fromkeys(fill_arr.shape
                                                          for fill_arr in self.polyfill_lat))).replace("[", "").replace("]",
                                                                                                                        "").replace("), (", "),(")
        unique_polyfill_lon_dims = str(list(dict.fromkeys(fill_arr.shape
                                                          for fill_arr in self.polyfill_lon))).replace("[", "").replace("]",
                                                                                                                        "").replace("), (", "),(")
        unique_elevation_dims = str(list(dict.fromkeys(el.shape for el in self.elevation))).replace("[", "").replace("]", "").replace("), (", "),(")

        polyfill_lat_str = "array(dims=%s, dtype=%s)" % (unique_polyfill_lat_dims, self.polyfill_lat[0].dtype)
        polyfill_lon_str = "array(dims=%s, dtype=%s)" % (unique_polyfill_lon_dims, self.polyfill_lon[0].dtype)
        elevation_str = "array(dims=%s, dtype=%s)" % (unique_elevation_dims, self.elevation[0].dtype)

        return "MosaicSkymap(polyfill_lat=%s, polyfill_lon=%s, elevation=%s, site_uid_list=%s)" % (
            polyfill_lat_str,
            polyfill_lon_str,
            elevation_str,
            self.site_uid_list.__repr__(),
        )


@dataclass
class MosaicData:
    """
    Prepared image data for use by mosaic routines.

    Attributes:
        site_uid_list (List[str]): 
            List of site unique identifiers contained within this object.
        timestamps (List[datetime.datetime]): 
            Timestamps of corresponding images.
        images (Dict[str, numpy.ndarray]): 
            Image data prepared into the necessary format; a dictionary. Keys are the site UID, 
            ndarray is the prepared data.
        images_dimensions (Dict[str, Tuple]): 
            The image dimensions.
        data_types (List[str]): 
            The data types for each data object.    
    """

    site_uid_list: List[str]
    timestamps: List[datetime.datetime]
    images: Dict[str, ndarray]
    images_dimensions: Dict[str, Tuple]
    data_types: List[str]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        unique_dimensions = str(list(dict.fromkeys(self.images_dimensions.values()))).replace("[", "").replace("]", "").replace("), (", "),(")
        images_str = "Dict[%d sites of array(dims=%s)]" % (len(self.images.keys()), unique_dimensions)
        timestamps_str = "[%d timestamps]" % (len(self.timestamps))

        return "MosaicData(images=%s, timestamps=%s, site_uid_list=%s)" % (images_str, timestamps_str, self.site_uid_list.__repr__())


@dataclass
class Mosaic:
    """
    Class representation for a generated mosaic.

    Attributes:
        polygon_data (matplotlib.collections.PolyCollection): 
            Generated polygons containing rendered data.

        cartopy_projection (cartopy.crs.Projection): 
            Cartopy projection to utilize.

        contour_data (Dict[str, List[Any]]): 
            Generated contour data.

        spect_cmap (str): 
            String giving the cmap to use for spect legend.
            
        spect_intensity_scale (Tuple[int]): 
            The min and max values that spectrograph data
            is scaled to in the mosaic, if any is present.
    """
    polygon_data: Union[PolyCollection, List[PolyCollection]]
    cartopy_projection: Projection
    contour_data: Optional[Dict[str, List[Any]]] = None
    spect_cmap: Optional[str] = None
    spect_intensity_scale: Optional[Tuple[int, int]] = None

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        if isinstance(self.polygon_data, list):
            polycollection_str = "[PolyCollection(...), ...]"
        else:
            polycollection_str = "PolyCollection(...)"

        if self.contour_data is not None:
            return "Mosaic(polygon_data=PolyCollection(...), cartopy_projection=Projection(%s), %s Contours)" % (
                self.cartopy_projection.to_string(),
                len(self.contour_data.get("x", [])),
            )
        else:
            return "Mosaic(polygon_data=" + polycollection_str + ", cartopy_projection=Projection(%s))" % (self.cartopy_projection.to_string())

    def plot(self,
             map_extent: Sequence[Union[float, int]],
             figsize: Optional[Tuple[int, int]] = None,
             rayleighs: bool = False,
             max_rayleighs: int = 20000,
             title: Optional[str] = None,
             colorbar_title: Optional[str] = None,
             ocean_color: Optional[str] = None,
             land_color: str = "gray",
             land_edgecolor: str = "#8A8A8A",
             borders_color: str = "#AEAEAE",
             borders_disable: bool = False,
             cbar_colormap: str = "",
             returnfig: bool = False,
             savefig: bool = False,
             savefig_filename: Optional[str] = None,
             savefig_quality: Optional[int] = None) -> Any:
        """
        Generate a plot of the mosaic data. 
        
        Either display it (default behaviour), save it to disk (using the `savefig` parameter), or 
        return the matplotlib plot object for further usage (using the `returnfig` parameter).

        Args:
            map_extent (List[int]): 
                Latitude/longitude range to be visible on the rendered map. This is a list of 4 integers 
                and/or floats, in the order of [min_lon, max_lon, min_lat, max_lat].

            figsize (tuple): 
                The matplotlib figure size to use when plotting. For example `figsize=(14,4)`.

            rayleighs (bool): 
                Set to `True` if the data being plotted is in Rayleighs. Defaults to `False`.

            max_rayleighs (int): 
                Max intensity scale for Rayleighs. Defaults to `20000`.

            ocean_color (str): 
                Colour of the ocean. Default is cartopy's default shade of blue. Colours can be supplied
                as a word, or hexcode prefixed with a '#' character (ie. `#55AADD`).
            
            land_color (str): 
                Colour of the land. Default is `gray`. Colours can be supplied as a word, or hexcode 
                prefixed with a '#' character (ie. `#41BB87`).

            land_edgecolor (str): 
                Color of the land edges. Default is `#8A8A8A`. Colours can be supplied as a word, or
                hexcode prefixed with a '#' character.

            borders_color (str): 
                Color of the country borders. Default is `AEAEAE`. Colours can be supplied as a word, or
                hexcode prefixed with a '#' character.
            
            borders_disable (bool): 
                Disbale rendering of the borders. Default is `False`.

            cbar_colorcmap (str): 
                The matplotlib colormap to use for the plotted color bar. Default is `gray`, unless
                mosaic was created with spectrograph data, in which case defaults to the colormap
                used for spectrograph data..

                Commonly used colormaps are:

                - REGO: `gist_heat`
                - THEMIS ASI: `gray`
                - TREx Blue: `Blues_r`
                - TREx NIR: `gray`
                - TREx RGB: `None`

                A list of all available colormaps can be found on the 
                [matplotlib documentation](https://matplotlib.org/stable/gallery/color/colormap_reference.html).

            returnfig (bool): 
                Instead of displaying the image, return the matplotlib figure object. This allows for further plot 
                manipulation, for example, adding labels or a title in a different location than the default. 
                
                Remember - if this parameter is supplied, be sure that you close your plot after finishing work 
                with it. This can be achieved by doing `plt.close(fig)`. 
                
                Note that this method cannot be used in combination with `savefig`.

            savefig (bool): 
                Save the displayed image to disk instead of displaying it. The parameter savefig_filename is required if 
                this parameter is set to True. Defaults to `False`.

            savefig_filename (str): 
                Filename to save the image to. Must be specified if the savefig parameter is set to True.

            savefig_quality (int): 
                Quality level of the saved image. This can be specified if the savefig_filename is a JPG image. If it
                is a PNG, quality is ignored. Default quality level for JPGs is matplotlib/Pillow's default of 75%.

        Returns:
            The displayed montage, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
            set to True, the plotting variables `(fig, ax)` will be returned.

        Raises:
        """
        # check return mode
        if (returnfig is True and savefig is True):
            raise ValueError("Only one of returnfig or savefig can be set to True")
        if returnfig is True and (savefig_filename is not None or savefig_quality is not None):
            warnings.warn("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                          "removing the savefig option parameter(s) as they will be ignored.",
                          stacklevel=1)
        elif (savefig is False and (savefig_filename is not None or savefig_quality is not None)):
            warnings.warn("A savefig option parameter was supplied, but the savefig parameter is False. The " +
                          "savefig option parameters will be ignored.",
                          stacklevel=1)

        # Get colormap if there is spectrograph data
        if self.spect_cmap is not None:
            cbar_colormap = self.spect_cmap

        # initialize figure
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes((0, 0, 1, 1), projection=self.cartopy_projection)
        ax.set_extent(map_extent, crs=cartopy.crs.Geodetic())  # type: ignore

        # add ocean
        #
        # NOTE: we use the default ocean color
        if (ocean_color is not None):
            ax.add_feature(  # type: ignore
                cartopy.feature.OCEAN, facecolor=ocean_color, zorder=0)
        else:
            ax.add_feature(cartopy.feature.OCEAN, zorder=0)  # type: ignore

        # add land
        ax.add_feature(  # type: ignore
            cartopy.feature.LAND, facecolor=land_color, edgecolor=land_edgecolor, zorder=0)

        # add borders
        if (borders_disable is False):
            ax.add_feature(  # type: ignore
                cartopy.feature.BORDERS, edgecolor=borders_color, zorder=0)

        # add polygon data
        #
        # NOTE: it seems that when running this function a second time, the polygon
        # data is not too happy. So to handle this, we plot a copy of the polygon data
        if isinstance(self.polygon_data, list):
            for polygon_data in self.polygon_data:
                ax.add_collection(copy(polygon_data))
        else:
            ax.add_collection(copy(self.polygon_data))

        if self.contour_data is not None:
            for i in range(len(self.contour_data["x"])):
                ax.plot(self.contour_data["x"][i],
                        self.contour_data["y"][i],
                        color=self.contour_data["color"][i],
                        linewidth=self.contour_data["linewidth"][i],
                        linestyle=self.contour_data["linestyle"][i],
                        marker=self.contour_data["marker"][i],
                        zorder=self.contour_data["zorder"][i])

        # set title
        if (title is not None):
            ax.set_title(title)

        # add text
        if (rayleighs is True):
            if isinstance(self.polygon_data, list):
                raise ValueError("Rayleighs Keyword is currently not available for mosaics with multiple sets of data.")

            # Create a colorbar, in Rayleighs, that accounts for the scaling limit we applied
            cbar_ticks = [float(j) / 5. for j in range(0, 6)]
            cbar_ticknames = [str(int(max_rayleighs / 5) * j) for j in range(0, 6)]

            # Any pixels with the max Rayleigh value could be greater than it, so we include the plus sign
            cbar_ticknames[-1] += "+"
            self.polygon_data.set_cmap(cbar_colormap)
            cbar = plt.colorbar(self.polygon_data, shrink=0.5, ticks=cbar_ticks, ax=ax)
            cbar.ax.set_yticklabels(cbar_ticknames)
            plt.text(1.025,
                     0.5,
                     "Intensity (Rayleighs)",
                     fontsize=14,
                     transform=ax.transAxes,
                     va="center",
                     rotation="vertical",
                     weight="bold",
                     style="oblique")

        if (self.spect_cmap) is not None:

            if (self.spect_intensity_scale) is None:
                intensity_max = np.nan
                intensity_min = np.nan
            else:
                intensity_max = self.spect_intensity_scale[1]
                intensity_min = self.spect_intensity_scale[0]

            # Create a colorbar, in Rayleighs, that accounts for the scaling limit we applied
            cbar_ticks = [float(j) / 5. for j in range(0, 6)]
            cbar_ticknames = [str(int((intensity_max / 5) + intensity_min) * j) for j in range(0, 6)]

            # Any specrograph bins with the max intensity value could be greater than it, so we include the plus sign
            cbar_ticknames[-1] += "+"
            if isinstance(self.polygon_data, list):
                self.polygon_data[0].set_cmap(cbar_colormap)
            else:
                self.polygon_data.set_cmap(cbar_colormap)
            if isinstance(self.polygon_data, list):
                cbar = plt.colorbar(self.polygon_data[0], shrink=0.5, ticks=cbar_ticks, ax=ax)
            else:
                cbar = plt.colorbar(self.polygon_data, shrink=0.5, ticks=cbar_ticks, ax=ax)
            cbar.ax.set_yticklabels(cbar_ticknames)
            if colorbar_title is None:
                plt.text(1.025,
                         0.5,
                         "Spectrograph Intensity (Rayleighs)",
                         fontsize=10,
                         transform=ax.transAxes,
                         va="center",
                         rotation="vertical",
                         weight="bold",
                         style="oblique")
            else:
                plt.text(1.025,
                         0.5,
                         colorbar_title,
                         fontsize=10,
                         transform=ax.transAxes,
                         va="center",
                         rotation="vertical",
                         weight="bold",
                         style="oblique")

        # save figure or show it
        if (savefig is True):
            # check that filename has been set
            if (savefig_filename is None):
                raise ValueError("The savefig_filename parameter is missing, but required since savefig was set to True.")

            # save the figure
            f_extension = os.path.splitext(savefig_filename)[-1].lower()
            if (".jpg" == f_extension or ".jpeg" == f_extension):
                # check quality setting
                if (savefig_quality is not None):
                    plt.savefig(savefig_filename, quality=savefig_quality, bbox_inches="tight")
                else:
                    plt.savefig(savefig_filename, bbox_inches="tight")
            else:
                if (savefig_quality is not None):
                    # quality specified, but output filename is not a JPG, so show a warning
                    warnings.warn("The savefig_quality parameter was specified, but is only used for saving JPG files. The " +
                                  "savefig_filename parameter was determined to not be a JPG file, so the quality will be ignored",
                                  stacklevel=1)
                plt.savefig(savefig_filename, bbox_inches="tight")

            # clean up by closing the figure
            plt.close(fig)
        elif (returnfig is True):
            # return the figure and axis objects
            return (fig, ax)
        else:
            # show the figure
            plt.show(fig)

            # cleanup by closing the figure
            plt.close(fig)

        # return
        return None

    def add_geo_contours(self,
                         lats: Optional[Union[ndarray, list]] = None,
                         lons: Optional[Union[ndarray, list]] = None,
                         constant_lats: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         constant_lons: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         color: str = "black",
                         linewidth: Union[float, int] = 1,
                         linestyle: str = "solid",
                         marker: str = "",
                         bring_to_front: bool = False):
        """
        Add geographic contours to a mosaic.

        Args:
            lats (ndarray or list):
                Sequence of geographic latitudes defining a contour.
            
            lons (ndarray or list):
                Sequence of geographic longitudes defining a contour.

            constant_lats (float, int, or Sequence):
                Geographic Latitude(s) at which to add line(s) of constant latitude.
            
            constant_lons (float, int, or Sequence):
                Geographic Longitude(s) at which to add line(s) of constant longitude.

            color (str):
                The matplotlib color used for the contour(s).

            linewidth (float or int):
                The contour thickness.
            
            linestyle (str):
                The matplotlib linestyle used for the contour(s).

            marker (str):
                The matplotlib marker used for the contour(s).

        Returns:
            The object's contour_data parameter is populated appropriately.

        Raises:
            ValueError: issues encountered with supplied parameters.
        """
        # Make sure some form of lat/lon is provided
        if (constant_lats is None) and (constant_lons is None) and (lats is None) and (lons is None):
            raise ValueError("No latitudes or longitudes provided.")

        # If manually passing in lats & lons, make sure both are provided
        if (lats is not None or lons is not None) and (lats is None or lons is None):
            raise (ValueError("Manually supplying contour requires both lats and lons."))

        # Check that color exists in matplotlib
        if color not in matplotlib.colors.CSS4_COLORS:
            raise ValueError(f"Color '{color}' not recognized by matplotlib.")

        # Check that linestyle is valid
        if linestyle not in ["-", "--", "-.", ":", "solid", "dashed", "dashdot", "dotted"]:
            raise ValueError(f"Linestyle '{linestyle}' not recognized by matplotlib.")

        # Check that linewidth is valid
        if linewidth <= 0:
            raise ValueError("Linewidth must be greater than zero.")

        # Check that marker is valid
        if marker not in ["", "o", ".", "p", "*", "x", "+", "X"]:
            raise ValueError(f"Marker '{marker}' is not currently supported.")

        # Convert numerics to lists if necessary
        if constant_lats is not None:
            if isinstance(constant_lats, (float, int)):
                constant_lats = [constant_lats]
        if constant_lons is not None:
            if isinstance(constant_lons, (float, int)):
                constant_lons = [constant_lons]

        # Initialize contour data dict if it doesn't exist yet
        if self.contour_data is None:
            self.contour_data = {"x": [], "y": [], "color": [], "linewidth": [], "linestyle": [], "marker": [], "zorder": []}

        # Obtain the mosaic's projection
        source_proj = pyproj.CRS.from_user_input(cartopy.crs.Geodetic())
        mosaic_proj = pyproj.CRS.from_user_input(self.cartopy_projection)
        transformer = pyproj.Transformer.from_crs(source_proj, mosaic_proj, always_xy=True)

        # First handling manually supplied lat/lon arrays
        if (lats is not None) and (lons is not None):
            # Convert lists to ndarrays if necessary
            if isinstance(lats, list):
                lats = np.array(lats)
            if isinstance(lons, list):
                lons = np.array(lons)

            if len(lats) != len(lons):
                raise ValueError("Lat/Lon data must be of the same size.")

            # Create specified contour from geographic coords
            x, y = transformer.transform(lons, lats)
            # Add contour to dict, along with color and linewidth
            self.contour_data["x"].append(x)
            self.contour_data["y"].append(y)
            self.contour_data["color"].append(color)
            self.contour_data["linewidth"].append(linewidth)
            self.contour_data["linestyle"].append(linestyle)
            self.contour_data["marker"].append(marker)
            self.contour_data["zorder"].append(int(bring_to_front))

        # Next handling lines of constant latitude
        if constant_lats is not None:
            # Generate longitudinal domain of the lat line (full globe)
            lon_domain = np.arange(-180, 180 + 0.2, 0.2)

            # Iterate through all lines of constant lat requested
            for lat in constant_lats:
                # Create line of constant lat
                const_lat_x, const_lat_y = (lon_domain, lon_domain * 0 + lat)
                sort_idx = np.argsort(const_lat_x)
                const_lat_y = const_lat_y[sort_idx]
                const_lat_x = const_lat_x[sort_idx]
                const_lat_x, const_lat_y = transformer.transform(const_lat_x, const_lat_y)
                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lat_x)
                self.contour_data["y"].append(const_lat_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))

        # Now handling lines of constant longitude
        if constant_lons is not None:
            # Generate latitudinal domain of the lon line (full globe)
            lat_domain = np.arange(-90, 90 + 0.1, 0.1)

            # Iterate through all lines of constant lon requested
            for lon in constant_lons:
                # Create line of constant lon and add to dict
                const_lon_x, const_lon_y = (lat_domain * 0 + lon, lat_domain)
                sort_idx = np.argsort(const_lon_y)
                const_lon_x = const_lon_x[sort_idx]
                const_lon_y = const_lon_y[sort_idx]
                const_lon_x, const_lon_y = transformer.transform(const_lon_x, const_lon_y)

                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lon_x)
                self.contour_data["y"].append(const_lon_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))

    def add_mag_contours(self,
                         timestamp: datetime.datetime,
                         constant_lats: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         constant_lons: Optional[Union[float, int, Sequence[Union[float, int]], ndarray]] = None,
                         lats: Optional[Union[ndarray, list]] = None,
                         lons: Optional[Union[ndarray, list]] = None,
                         color: str = "black",
                         linewidth: Union[float, int] = 1,
                         linestyle: str = "solid",
                         marker: str = "",
                         bring_to_front: bool = False):
        """
        Add geomagnetic contours to a mosaic.

        Args:
            timestamp (datetime.datetime):
                The timestamp used in computing AACGM coordinates.

            lats (ndarray or list):
                Sequence of geomagnetic latitudes defining a contour.
            
            lons (ndarray or list):
                Sequence of geomagnetic longitudes defining a contour.

            constant_lats (float, int, Sequence):
                Geomagnetic latitude(s) at which to add contour(s) of constant latitude.
            
            constant_lons (float, int, Sequence):
                Geomagnetic longitude(s) at which to add contours(s) of constant longitude.

            color (str):
                The matplotlib color used for the contour(s).

            linewidth (float or int):
                The contour thickness.

            linestyle (str):
                The matplotlib linestyle used for the contour(s).

            marker (str):
                The matplotlib marker used for the contour(s).

        Returns:
            The object's contour_data parameter is populated appropriately.

        Raises:
            ValueError: issues encountered with supplied parameters.
        """
        # Make sure some form of lat/lon is provided
        if (constant_lats is None) and (constant_lons is None) and (lats is None) and (lons is None):
            raise ValueError("No latitudes or longitudes provided.")

        # If manually passing in lats & lons, make sure both are provided
        if (lats is not None or lons is not None) and (lats is None or lons is None):
            raise (ValueError("Manually supplying contour requires both lats and lons."))

        # Check that color exists in matplotlib
        if color not in matplotlib.colors.CSS4_COLORS:
            raise ValueError(f"Color '{color}' not recognized by matplotlib.")

        # Check that linestyle is valid
        if linestyle not in ["-", "--", "-.", ":", "solid", "dashed", "dashdot", "dotted"]:
            raise ValueError(f"Linestyle '{linestyle}' not recognized by matplotlib.")

        # Check that linewidth is valid
        if linewidth <= 0:
            raise ValueError("linewidth must be greater than zero.")

        # Convert numerics to lists if necessary
        if constant_lats is not None:
            if isinstance(constant_lats, (float, int)):
                constant_lats = [constant_lats]
        if constant_lons is not None:
            if isinstance(constant_lons, (float, int)):
                constant_lons = [constant_lons]

        # Initialize contour data dict if it doesn't exist yet
        if self.contour_data is None:
            self.contour_data = {"x": [], "y": [], "color": [], "linewidth": [], "linestyle": [], "marker": [], "zorder": []}

        # Obtain the mosaic's projection
        source_proj = pyproj.CRS.from_user_input(cartopy.crs.Geodetic())
        mosaic_proj = pyproj.CRS.from_user_input(self.cartopy_projection)
        transformer = pyproj.Transformer.from_crs(source_proj, mosaic_proj, always_xy=True)

        # First handling manually supplied lat/lon arrays
        if (lats is not None) and (lons is not None):
            # Convert lists to ndarrays if necessary
            if isinstance(lats, list):
                lats = np.array(lats)
            if isinstance(lons, list):
                lons = np.array(lons)

            if len(lats) != len(lons):
                raise ValueError("Lat/Lon data must be of the same size.")

            # Create specified contour from magnetic coords
            y, x, alt = aacgmv2.convert_latlon_arr(lats, lons, lats * 0.0, timestamp, method_code="A2G")
            x, y = transformer.transform(x, y)
            # Add contour to dict, along with color and linewidth
            self.contour_data["x"].append(x)
            self.contour_data["y"].append(y)
            self.contour_data["color"].append(color)
            self.contour_data["linewidth"].append(linewidth)
            self.contour_data["linestyle"].append(linestyle)
            self.contour_data["marker"].append(marker)
            self.contour_data["zorder"].append(int(bring_to_front))

        # Next handling lines of constant latitude
        if constant_lats is not None:
            # Generate longitudinal domain of the lat line (full globe)
            lon_domain = np.arange(-180, 180 + 0.2, 0.2)

            # iterate through all lines of constant lat requested
            for lat in constant_lats:
                # Create line of constant lat from magnetic coords
                const_lat_x, const_lat_y = (lon_domain, lon_domain * 0 + lat)
                const_lat_y, const_lat_x, alt = aacgmv2.convert_latlon_arr(const_lat_y, const_lat_x, const_lat_x * 0.0, timestamp, method_code="A2G")
                sort_idx = np.argsort(const_lat_x)
                const_lat_y = const_lat_y[sort_idx]
                const_lat_x = const_lat_x[sort_idx]
                const_lat_x, const_lat_y = transformer.transform(const_lat_x, const_lat_y)

                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lat_x)
                self.contour_data["y"].append(const_lat_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))

        # Now handling lines of constant longitude
        if constant_lons is not None:
            # Generate latitudinal domain of the lon line (full globe)
            lat_domain = np.arange(-90, 90 + 0.1, 0.1)

            # iterate through all lines of constant lon requested
            for lon in constant_lons:
                # Create line of constant lon from magnetic coords
                const_lon_x, const_lon_y = (lat_domain * 0 + lon, lat_domain)
                const_lon_y, const_lon_x, alt = aacgmv2.convert_latlon_arr(const_lon_y, const_lon_x, const_lon_x * 0.0, timestamp, method_code="A2G")
                sort_idx = np.argsort(const_lon_y)
                const_lon_x = const_lon_x[sort_idx]
                const_lon_y = const_lon_y[sort_idx]
                const_lon_x, const_lon_y = transformer.transform(const_lon_x, const_lon_y)

                # Add contour to dict, along with color and linewidth
                self.contour_data["x"].append(const_lon_x)
                self.contour_data["y"].append(const_lon_y)
                self.contour_data["color"].append(color)
                self.contour_data["linewidth"].append(linewidth)
                self.contour_data["linestyle"].append(linestyle)
                self.contour_data["marker"].append(marker)
                self.contour_data["zorder"].append(int(bring_to_front))
