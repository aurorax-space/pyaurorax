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
Work with spectrograph data.
"""

import datetime
from typing import Union, List, Optional, Tuple, Any
from ...data.ucalgary import Data
from ._plot import plot as func_plot

__all__ = ["SpectraManager"]


class SpectraManager:
    """
    The SpectraManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self):
        pass

    def plot(self,
             spect_data: Data,
             timestamp: Union[datetime.datetime, List[
                 datetime.datetime,
             ]],
             spect_loc: Union[int, List[int]],
             title: Optional[str] = None,
             figsize: Optional[Tuple[int, int]] = None,
             color: Optional[Union[str, List]] = None,
             ylog: bool = False,
             xlabel: str = "Wavelength (nm)",
             ylabel: str = "Intensity (R/nm)",
             ylim: Optional[Tuple[int, int]] = None,
             xlim: Optional[Tuple[int, int]] = None,
             plot_line: Optional[Union[float, List[float]]] = None,
             plot_line_color: Optional[Union[str, List[str]]] = None,
             returnfig: bool = False,
             savefig: bool = False,
             savefig_filename: Optional[str] = None,
             savefig_quality: Optional[int] = None) -> Any:
        """
        Generate a plot of one or more spectra from spectrograph data. 
        
        Either display it (default behaviour), save it to disk (using the `savefig` parameter), or 
        return the matplotlib plot object for further usage (using the `returnfig` parameter).

        Args:
            spect_data (pyaurorax.data.ucalgary.Data): 
                The data object containing spectrograph data.

            timestamp (datetime.datetime): 
                A timestamp or list of timestamps for which to plot spectra from.

            spect_loc (int): 
                An int or list of ints giving the spectrograph spatial bin indices to plot.

            title (str): 
                The title to display above the plotted spectra.

            figsize (tuple): 
                The matplotlib figure size to use when plotting. For example `figsize=(14,4)`.

            color (str, List): 
                A string or list of strings giving the matplotlib color names to use for plotting spectra.

            ylog (bool): 
                Plot on a logarithmic axis. Default is linear.

            xlabel (str): 
                The x-axis label to use. Default is `Wavelength (nm)`.

            ylabel (str): 
                The y-axis label to use. Default is 'Intensity (Rayleighs)'.

            ylim (Tuple[int]): 
                The min and max values to display on the y-axis, in units of Rayleighs/nm.

            xlim (Tuple[int]): 
                The min and max values to display on the x-axis, in units of nm.

            plot_line (float): 
                A float, or list of floats, giving wavelengths at which to plot a vertical line, useful for comparing
                to known emission wavelengths (e.g. 557.7).

            plot_line_color (str): 
                A string or list of strings giving the colors to use for plotting lines specified by 'plot_lines'.

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
            The displayed spectra, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
            set to True, the plotting variables `(fig, ax)` will be returned.

        Raises:
            ValueError: issues encountered with supplied parameters
        """
        return func_plot(spect_data, timestamp, spect_loc, title, figsize, color, ylog, xlabel, ylabel, ylim, xlim, plot_line, plot_line_color,
                         returnfig, savefig, savefig_filename, savefig_quality)
