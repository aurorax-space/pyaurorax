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
Class representation for a keogram.
"""

import os
import datetime
import warnings
import aacgmv2
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple, Literal, Union, Any
from ...data.ucalgary import Skymap


@dataclass
class Keogram:
    """
    Class representation for a keogram

    Attributes:
        data (numpy.ndarray): 
            The derived keogram data.
        timestamp (List[datetime.datetime]): 
            Timestamps corresponding to each keogram slice.
        instrument_type (str):
            String giving instrument type, either 'asi' or 'spectrograph'.
        ccd_y (numpy.ndarray): 
            The y-axis representing CCD Y coordinates for the keogram.
        mag_y (numpy.ndarray): 
            The y-axis representing magnetic latitude for the keogram.
        geo_y (numpy.ndarray): 
            The y-axis representing geographic latitude for the keogram.
    """

    def __init__(self,
                 data: np.ndarray,
                 timestamp: List[datetime.datetime],
                 instrument_type: str,
                 slice_idx: Optional[int] = None,
                 ccd_y: Optional[np.ndarray] = None,
                 mag_y: Optional[np.ndarray] = None,
                 geo_y: Optional[np.ndarray] = None):
        # public vars
        self.data = data
        self.timestamp = timestamp
        self.instrument_type = instrument_type
        self.ccd_y = ccd_y
        self.mag_y = mag_y
        self.geo_y = geo_y

        # private vars
        self.__slice_idx = slice_idx

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        data_str = "array(dims=%s, dtype=%s)" % (self.data.shape, self.data.dtype)
        timestamp_str = "[%d datetime objects]" % (len(self.timestamp))
        ccd_y_str = "None" if self.ccd_y is None else "array(%d values)" % (self.ccd_y.shape[0])
        mag_y_str = "None" if self.mag_y is None else "array(%d values)" % (self.mag_y.shape[0])
        geo_y_str = "None" if self.geo_y is None else "array(%d values)" % (self.geo_y.shape[0])

        return "Keogram(data=%s, timestamp=%s, ccd_y=%s, mag_y=%s, geo_y=%s)" % (data_str, timestamp_str, ccd_y_str, mag_y_str, geo_y_str)

    def set_geographic_latitudes(self, skymap: Skymap, altitude_km: Optional[Union[int, float]] = None) -> None:
        """
        Set the geographic latitude values for this keogram, using the specified skymap 
        data. The data will be set to the geo_y attribute of this Keogram object, which
        can then be used for plotting and/or further analysis.

        Args:
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap object to use. This parameter is required.

            altitude_km (int): 
                The altitude to use, in kilometers. If not specified, it will use the default in the 
                skymap object. If the specified altitude is not valid, a ValueError will be raised.
        
        Returns:
            None. The Keogram object's `geo_y` attribute will be updated.

        Raises:
            ValueError: Issues with specified altitude.
        """
        # check for slice idx
        if (self.__slice_idx is None):
            raise ValueError("Unable to set the geographic latitudes since the slice_idx is None. If this keogram " +
                             "object was created as part of the custom_keogram routines or is a spectrogaph keogram, " +
                             "this is expected and performing this action is not supported at this time.")

        # determine altitude index to use
        if (altitude_km is not None):
            # Obtain lat/lon arrays from skymap
            if (altitude_km * 1000.0 in skymap.full_map_altitude):
                altitude_idx = np.where(altitude_km * 1000.0 == skymap.full_map_altitude)

                self.geo_y = np.squeeze(skymap.full_map_latitude[altitude_idx, :, self.__slice_idx]).copy()
            else:
                # Make sure altitude is in range that can be interpolated
                if (altitude_km * 1000.0 < skymap.full_map_altitude[0]) or (altitude_km * 1000.0 > skymap.full_map_altitude[2]):
                    raise ValueError("Altitude " + str(altitude_km) + " outside valid range of " +
                                     str((skymap.full_map_altitude[0] / 1000.0, skymap.full_map_altitude[2] / 1000.0)))

                # Initialze empty lat/lon arrays
                lats = np.full(np.squeeze(skymap.full_map_latitude[0, :, :]).shape, np.nan, dtype=skymap.full_map_latitude[0, :, :].dtype)

                # Interpolate lats and lons at desired altitude
                for i in range(skymap.full_map_latitude.shape[1]):
                    for j in range(skymap.full_map_latitude.shape[2]):
                        lats[i, j] = np.interp(altitude_km * 1000.0, skymap.full_map_altitude, skymap.full_map_latitude[:, i, j])

                self.geo_y = lats[:, self.__slice_idx].copy()
        else:
            # use default middle altitude
            self.geo_y = np.squeeze(skymap.full_map_latitude[1, :, self.__slice_idx]).copy()

    def set_magnetic_latitudes(self, skymap: Skymap, timestamp: datetime.datetime, altitude_km: Optional[Union[int, float]] = None) -> None:
        """
        Set the magnetic latitude values for this keogram, using the specified skymap 
        data. AACGMv2 will be utilized to perform the calculations. The resulting data
        will be set to the mag_y attribute of this Keogram object, which can then be
        used for plotting and/or further analysis.

        Args:
            skymap (pyaurorax.data.ucalgary.Skymap): 
                The skymap object to use. This parameter is required.

            timestamp (datetime.datetime): 
                The timestamp to use when converting skymap data to magnetic coordinates. Utilizes
                AACGMv2 to do the conversion.

            altitude_km (int): 
                The altitude to use. If not specified, it will use the default in the skymap
                object. If the specified altitude is not valid, a ValueError will be raised.
        
        Returns:
            None. The Keogram object's `mag_y` attribute will be updated.

        Raises:
            ValueError: Issues with specified altitude.
        """
        # check for slice idx
        if (self.__slice_idx is None):
            raise ValueError("Unable to set the geographic latitudes since the slice_idx is None. If this keogram " +
                             "object was created as part of the custom_keogram routines or is a spectrogaph keogram, " +
                             "this is expected and performing this action is not supported at this time.")

        # determine altitude index to use
        if (altitude_km is not None):
            # Obtain lat/lon arrays from skymap
            if (altitude_km * 1000.0 in skymap.full_map_altitude):
                altitude_idx = np.where(altitude_km * 1000.0 == skymap.full_map_altitude)

                lats = np.squeeze(skymap.full_map_latitude[altitude_idx, :, :])
                lons = np.squeeze(skymap.full_map_longitude[altitude_idx, :, :])
                lons[np.where(lons > 180)] -= 360.0

            else:
                # Make sure altitude is in range that can be interpolated
                if (altitude_km * 1000.0 < skymap.full_map_altitude[0]) or (altitude_km * 1000.0 > skymap.full_map_altitude[2]):
                    raise ValueError("Altitude " + str(altitude_km) + " outside valid range of " +
                                     str((skymap.full_map_altitude[0] / 1000.0, skymap.full_map_altitude[2] / 1000.0)))

                # Initialze empty lat/lon arrays
                lats = np.full(np.squeeze(skymap.full_map_latitude[0, :, :]).shape, np.nan, dtype=skymap.full_map_latitude[0, :, :].dtype)
                lons = lats.copy()

                # Interpolate lats and lons at desired altitude
                for i in range(skymap.full_map_latitude.shape[1]):
                    for j in range(skymap.full_map_latitude.shape[2]):
                        lats[i, j] = np.interp(altitude_km * 1000.0, skymap.full_map_altitude, skymap.full_map_latitude[:, i, j])
                        lons[i, j] = np.interp(altitude_km * 1000.0, skymap.full_map_altitude, skymap.full_map_longitude[:, i, j])

                lons[np.where(lons > 180)] -= 360.0

            # Convert lats and lons to geomagnetic coordinates
            mag_lats, mag_lons, mag_alts = aacgmv2.convert_latlon_arr(lats.flatten(),
                                                                      lons.flatten(), (lons * 0.0).flatten(),
                                                                      timestamp,
                                                                      method_code='G2A')
            mag_lats = np.reshape(mag_lats, lats.shape)
            mag_lons = np.reshape(mag_lons, lons.shape)

            # Set the y axis to the desired slice index of the magnetic latitudes
            self.mag_y = mag_lats[:, self.__slice_idx].copy()
        else:
            # Convert middle altitude lats and lons to geomagnetic coordinates
            mag_lats, mag_lons, mag_alts = aacgmv2.convert_latlon_arr(np.squeeze(skymap.full_map_latitude[1, :, :]).flatten(),
                                                                      np.squeeze(skymap.full_map_longitude[1, :, :]).flatten(),
                                                                      (skymap.full_map_longitude[1, :, :] * 0.0).flatten(),
                                                                      timestamp,
                                                                      method_code='G2A')
            mag_lats = np.reshape(mag_lats, np.squeeze(skymap.full_map_latitude[1, :, :]).shape)
            mag_lons = np.reshape(mag_lons, np.squeeze(skymap.full_map_longitude[1, :, :]).shape)

            # Set the y axis to the desired slice index of the magnetic latitudes
            self.mag_y = mag_lats[:, self.__slice_idx].copy()

    def plot(self,
             y_type: Literal["ccd", "mag", "geo"] = "ccd",
             title: Optional[str] = None,
             figsize: Optional[Tuple[int, int]] = None,
             cmap: Optional[str] = None,
             aspect: Optional[Union[Literal["equal", "auto"], float]] = None,
             axes_visible: bool = True,
             xlabel: str = "Time (UTC)",
             ylabel: Optional[str] = None,
             xtick_increment: Optional[int] = None,
             ytick_increment: Optional[int] = None,
             returnfig: bool = False,
             savefig: bool = False,
             savefig_filename: Optional[str] = None,
             savefig_quality: Optional[int] = None) -> Any:
        """
        Generate a plot of the keogram data. 
        
        Either display it (default behaviour), save it to disk (using the `savefig` parameter), or 
        return the matplotlib plot object for further usage (using the `returnfig` parameter).

        Args:
            y_type (str): 
                Type of y-axis to use when plotting. Options are `ccd`, `mag`, or `geo`. The
                default is `ccd`. This parameter is required.

            title (str): 
                The title to display above the plotted keogram.

            figsize (tuple): 
                The matplotlib figure size to use when plotting. For example `figsize=(14,4)`.

            cmap (str): 
                The matplotlib colormap to use.

                Commonly used colormaps are:

                - REGO: `gist_heat`
                - THEMIS ASI: `gray`
                - TREx Blue: `Blues_r`
                - TREx NIR: `gray`
                - TREx RGB: `None`

                A list of all available colormaps can be found on the 
                [matplotlib documentation](https://matplotlib.org/stable/gallery/color/colormap_reference.html).
            
            aspect (str or float): 
                The matplotlib imshow aspect ration to use. A common value for this is `auto`. All valid values 
                can be found on the [matplotlib documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html).

            axes_visible (bool): 
                Display the axes. Default is `True`.

            xlabel (str): 
                The x-axis label to use. Default is `Time (UTC)`.

            ylabel (str): 
                The y-axis label to use. Default is based on y_type.

            xtick_increment (int): 
                The x-axis tick increment to use. Default is 100.

            ytick_increment (int): 
                The y-axis tick increment to use. Default is 50.

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
            The displayed keogram, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
            set to True, the plotting variables `(fig, ax)` will be returned.

        Raises:
            ValueError: Issues with the y-axis choice.
        """
        # check return mode
        if (returnfig is True and savefig is True):
            raise ValueError("Only one of returnfig or savefig can be set to True")
        if returnfig is True and (savefig_filename is not None or savefig_quality is not None):
            warnings.warn("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                          "removing the savefig option parameter(s) as they will be ignored.",
                          stacklevel=1)
        elif savefig is False and (savefig_filename is not None or savefig_quality is not None):
            warnings.warn("A savefig option parameter was supplied, but the savefig parameter is False. The " +
                          "savefig option parameters will be ignored.",
                          stacklevel=1)

        # init figure and plot data
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes((0, 0, 1, 1))
        ax.imshow(self.data, origin="lower", cmap=cmap, aspect=aspect)

        # set title
        if (title is not None):
            ax.set_title(title)

        # set axes
        if (axes_visible is True):
            # do checks for y-axis that was chosen
            if (y_type == "geo" and self.geo_y is None):
                raise ValueError("Unable to plot using geo_y data. The geo_y attribute is currently None, so either populate "
                                 "it with data using the set_geographic_latitudes() function, or choose a different y_type")
            elif (y_type == "mag" and self.mag_y is None):
                raise ValueError("Unable to plot using mag_y data. The mag_y attribute is currently None, so either populate "
                                 "it with data using the set_magnetic_latitudes() function, or choose a different y_type")

            # set y axis data, and y label
            y_axis_data = self.ccd_y
            if (y_type == "mag"):
                y_axis_data = self.mag_y
                if (ylabel is None):
                    ylabel = "Magnetic latitude"
            elif (y_type == "geo"):
                y_axis_data = self.geo_y
                if (ylabel is None):
                    ylabel = "Geographic latitude"
            else:
                if (ylabel is None):
                    ylabel = "CCD Y"

            # print labels
            ax.set_xlabel(xlabel, fontsize=14)
            ax.set_ylabel(ylabel, fontsize=14)

            # generate x ticks and labels
            #
            # TODO: make this more dynamic
            if (xtick_increment is None):
                xtick_increment = 100  # assume data is 3 second cadence; good enough for now
            x_ticks = np.arange(0, self.data.shape[1], xtick_increment)
            x_labels = self.timestamp[::xtick_increment]
            for i in range(0, len(x_labels)):
                x_labels[i] = x_labels[i].strftime("%H:%M")  # type: ignore
            ax.set_xticks(x_ticks, x_labels)  # type: ignore

            # do check for ccd_y
            if (self.ccd_y is None):
                warnings.warn(
                    "Unable to plot y-axis. If this keogram object was create as part of the custom_keogram " +
                    "routines, this is expected and plotting a custom keogram with axes is not supported at this time.",
                    stacklevel=1,
                )
            else:
                # generate y ticks and labels
                if (y_type == "ccd"):
                    # TODO: make this more dynamic
                    if (ytick_increment is None):
                        ytick_increment = 50

                    # generate y ticks and labels
                    y_ticks = y_axis_data[::ytick_increment]  # type: ignore
                    y_labels = y_axis_data[::ytick_increment]  # type: ignore

                    # apply yticks
                    ax.set_yticks(y_ticks, y_labels)  # type: ignore
                elif (y_type == "geo" and self.geo_y is not None) or (y_type == "mag" and self.mag_y is not None):
                    # set tick increments
                    if (ytick_increment is None):
                        ytick_increment = 50

                    # generate y ticks and labels
                    y_ticks = self.ccd_y[25::ytick_increment]
                    y_labels = np.round(
                        y_axis_data,  # type: ignore
                        1).astype(str)[25::ytick_increment]
                    y_labels[np.where(y_labels == 'nan')] = ''

                    # apply yticks
                    ax.set_yticks(y_ticks, y_labels)
        else:
            # disable axes
            ax.set_axis_off()

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
