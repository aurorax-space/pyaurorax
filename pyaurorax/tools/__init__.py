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
Data analysis toolkit for working with all-sky imager data available within the
AuroraX platform.

This portion of the PyAuroraX library allows you to easily generate basic plots
for ASI data, and common manipulations. These include things like displaying single
images, making keograms, projecting ASI data onto maps, and extracting metrics for
a given lat/lon bounding box.

Example:
    For shorter function calls, you can initialize the tools submodule using like so:

    ```
    import pyaurorax
    aurorax = pyaurorax.PyAuroraX()
    at = aurorax.tools
    ```
"""

# pull in classes
from .classes.keogram import Keogram
from .classes.montage import Montage
from .classes.mosaic import Mosaic, MosaicData, MosaicSkymap

# imports for this file
from .bounding_box import BoundingBoxManager
from .calibration import CalibrationManager
from .ccd_contour import CCDContourManager
from .grid_files import GridFilesManager
from .keogram import KeogramManager
from .montage import MontageManager
from .mosaic import MosaicManager
from .spectra import SpectraManager
from ._display import display as func_display
from ._movie import movie as func_movie
from ._scale_intensity import scale_intensity as func_scale_intensity
from ._util import set_theme as func_set_theme

# typing imports
import numpy as np
from typing import Literal, Optional, Tuple, Union, Any, List

__all__ = [
    "ToolsManager",
    "Keogram",
    "Montage",
    "Mosaic",
    "MosaicData",
    "MosaicSkymap",
]


class ToolsManager:
    """
    The ToolsManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

        # initialize sub-modules
        self.__bounding_box = BoundingBoxManager(self.__aurorax_obj)
        self.__calibration = CalibrationManager()
        self.__ccd_contour = CCDContourManager()
        self.__grid_files = GridFilesManager(self.__aurorax_obj)
        self.__keogram = KeogramManager()
        self.__montage = MontageManager()
        self.__mosaic = MosaicManager(self.__aurorax_obj)
        self.__spectra = SpectraManager()

    # ------------------------------------------
    # properties for submodule managers
    # ------------------------------------------
    @property
    def bounding_box(self):
        """
        Access to the `bounding_box` submodule from within a PyAuroraX object.
        """
        return self.__bounding_box

    @property
    def calibration(self):
        """
        Access to the `calibration` submodule from within a PyAuroraX object.
        """
        return self.__calibration

    @property
    def ccd_contour(self):
        """
        Access to the `ccd_contour` submodule from within a PyAuroraX object.
        """
        return self.__ccd_contour

    @property
    def grid_files(self):
        """
        Access to the `grid_files` submodule from within a PyAuroraX object.
        """
        return self.__grid_files

    @property
    def keogram(self):
        """
        Access to the `keogram` submodule from within a PyAuroraX object.
        """
        return self.__keogram

    @property
    def montage(self):
        """
        Access to the `montage` submodule from within a PyAuroraX object.
        """
        return self.__montage

    @property
    def mosaic(self):
        """
        Access to the `mosaic` submodule from within a PyAuroraX object.
        """
        return self.__mosaic

    @property
    def spectra(self):
        """
        Access to the `spectra` submodule from within a PyAuroraX object.
        """
        return self.__spectra

    # ------------------------------------------
    # functions available at this manager level
    # ------------------------------------------
    def display(self,
                image: np.ndarray,
                cmap: Optional[str] = None,
                figsize: Optional[Tuple[int, int]] = None,
                aspect: Optional[Union[Literal["equal", "auto"], float]] = None,
                colorbar: bool = False,
                title: Optional[str] = None,
                returnfig: bool = False,
                savefig: bool = False,
                savefig_filename: Optional[str] = None,
                savefig_quality: Optional[int] = None) -> Any:
        """
        Render a visualization of a single image.

        Either display it (default behaviour), save it to disk (using the `savefig` parameter), or 
        return the matplotlib plot object for further usage (using the `returnfig` parameter).

        Args:
            image (numpy.ndarray): 
                The image to display, represented as a numpy array.

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

            figsize (tuple): 
                The matplotlib figure size to use when displaying, tuple of two integers (ie. `figsize=(14, 4)`)
        
            aspect (str or float): 
                The matplotlib imshow aspect ration to use. A common value for this is `auto`. All valid values 
                can be found on the [matplotlib documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html).

            colorbar (bool): 
                Display a colorbar. Default is `False`.

            title (str): 
                A title to display above the rendered image. Defaults to no title.

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
            The displayed image, by default. If `savefig` is set to True, nothing will be returned. If `returnfig` is 
            set to True, the plotting variables `(fig, ax)` will be returned.

        Raises:
            ValueError: issues encountered with supplied parameters.
        """
        return func_display(image, cmap, figsize, aspect, colorbar, title, returnfig, savefig, savefig_filename, savefig_quality)

    def movie(
        self,
        input_filenames: List[str],
        output_filename: str,
        n_parallel: int = 1,
        fps: int = 25,
        progress_bar_disable: bool = False,
    ) -> None:
        """
        Generate a movie file from a list of filenames. Note that the codec used is "mp4v".

        Args:
            input_filenames (List[str]): 
                Filenames of frames to use for movie generation. No sorting is applied, so it is 
                assumed the list is in the desired order. This parameter is required.
            
            output_filename (str): 
                Filename for the created movie file. This parameter is required.

            n_parallel (int): 
                Number of multiprocessing workers to use. Default is `1`, which does not use
                multiprocessing.

            fps (int): 
                Frames per second (FPS) for the movie file. Default is `25`.

            progress_bar_disable (bool): 
                Toggle the progress bars off. Default is `False`.        

        Raises:
            IOError: I/O related issue while generating movie
        """
        return func_movie(self.__aurorax_obj, input_filenames, output_filename, n_parallel, fps, progress_bar_disable)

    def scale_intensity(
        self,
        data: np.ndarray,
        min: Optional[float] = None,
        max: Optional[float] = None,
        top: Optional[float] = None,
        memory_saver: bool = True,
    ) -> np.ndarray:
        """
        Scale all values of an array that lie in the range min<=x<=max in to 
        the range 0<=x<=top.
        
        Args:
            data (numpy.ndarray): 
                Data array, can be 2, 3, or 4-dimensional. Assumed to be an image, or array of 
                images. Also assumed that the first 2 dimensions are the image's x and y 
                coordinates, and the following dimensions are some combination of the number of 
                images, and/or the colour channel.

            min (float): 
                Minimum value of array to be considered

            max (float): 
                Maximum value of array to be considered

            top (float): 
                Maximum value of the scaled result. If not supplied, the max value
                of the data array's dtype is used.

            memory_saver (bool): 
                Utilize less RAM when scaling a set of images. Defaults to `True`. If set to `False` then
                the scaling routine will be faster, but will utilize significantly more RAM.

        Returns:
            A new `numpy.ndarray` that is the same dimensions as the inputted data array, 
            with the scaling applied.

        Raises:
            ValueError: issues encountered with supplied min, max, or top value(s)
        """
        return func_scale_intensity(data, min, max, top, memory_saver)

    def set_theme(self, theme: str) -> None:
        """
        A handy wrapper for setting the matplotlib global theme. Common choices are `light`, 
        `dark`, or `default`.

        Args:
            theme (str): 
                Theme name. Common choices are `light`, `dark`, or `default`. If default, then
                matplotlib theme settings will be fully reset to their defaults.

                Additional themes can be found on the 
                [matplotlib documentation](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html)
        """
        return func_set_theme(theme)
