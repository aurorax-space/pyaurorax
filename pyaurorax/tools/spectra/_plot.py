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

import os
import itertools
import numpy as np
import matplotlib.pyplot as plt
from ..._util import show_warning


def plot(
    spect_data,
    timestamp,
    spect_loc,
    title,
    figsize,
    color,
    ylog,
    xlabel,
    ylabel,
    ylim,
    xlim,
    plot_line,
    plot_line_color,
    returnfig,
    savefig,
    savefig_filename,
    savefig_quality,
):
    # check return mode
    if (returnfig is True and savefig is True):
        raise ValueError("Only one of returnfig or savefig can be set to True")
    if (returnfig is True and (savefig_filename is not None or savefig_quality is not None)):
        show_warning("The figure will be returned, but a savefig option parameter was supplied. Consider " +
                     "removing the savefig option parameter(s) as they will be ignored.",
                     stacklevel=1)
    elif (savefig is False and (savefig_filename is not None or savefig_quality is not None)):
        show_warning("A savefig option parameter was supplied, but the savefig parameter is False. The " +
                     "savefig option parameters will be ignored.",
                     stacklevel=1)

    # init figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes((0, 0, 1, 1))

    # Convert plot lines to list if required
    if plot_line is not None:
        if not isinstance(plot_line, list):
            plot_line = [plot_line]

    # Convert plot line colors to list if required
    if plot_line_color is not None:
        if not isinstance(plot_line_color, list):
            plot_line_color = [plot_line_color]
    else:
        # default plot lines to gray
        plot_line_color = []
        if plot_line is not None:
            for _i in range(len(plot_line)):
                plot_line_color = 'gray'

    # Plot the requested lines if any
    if plot_line is not None:
        for i, line in enumerate(plot_line):
            ax.plot([line, line], [-5000.0, 5000000.0], color=plot_line_color[i], linestyle='--')

    # Set up color cycle
    color_cycle = itertools.cycle(color) if isinstance(color, list) else itertools.cycle([color])

    # Convert input timestamps to list if required
    if not isinstance(timestamp, list):
        timestamp = [timestamp]

    # Convert input spatial bins to list if required
    if not isinstance(spect_loc, list):
        spect_loc = [spect_loc]

    # Automatically generate a default title, as
    # well as default legend labels to use
    auto_title = (f"{spect_data.metadata[0]['site_uid'].decode('utf-8').upper()} - "
                  f"{timestamp[0].strftime('%Y-%m-%d %H:%M:%S')} UTC (Spatial Bin {spect_loc[0]})")
    auto_legend = [None]
    if len(timestamp) != len(spect_loc):
        if (len(timestamp) != 1) and (len(spect_loc) != 1):
            raise ValueError("Inputs 'timestamp' and 'spect_loc' must have the same number of elements (or one must be of length 1).")

        elif (len(timestamp) > 1):
            single_spect_loc = spect_loc[0]
            spect_loc = []
            for _i in range(len(timestamp)):
                spect_loc.append(single_spect_loc)
            auto_title = f"{spect_data.metadata[0]['site_uid'].decode('utf-8').upper()} - Spatial Bin {spect_loc[0]}"
            auto_legend = []
            for i in range(len(timestamp)):
                auto_legend.append(f"{timestamp[i].strftime('%Y-%m-%d %H:%M:%S')} UTC")

        elif (len(spect_loc) > 1):
            single_timestamp = timestamp[0]
            timestamp = []
            for _i in range(len(spect_loc)):
                timestamp.append(single_timestamp)
            auto_title = f"{spect_data.metadata[0]['site_uid'].decode('utf-8').upper()} - {timestamp[0].strftime('%Y-%m-%d %H:%M:%S')} UTC"
            auto_legend = []
            for i in range(len(timestamp)):
                auto_legend.append(f"spatial bin {spect_loc[i]}")

        else:
            auto_title = f"{spect_data.metadata[0]['site_uid'].decode('utf-8').upper()} Spectrograph"
            auto_legend = []
            for _i in range(len(timestamp)):
                auto_legend.append(f"{timestamp[0].strftime('%Y-%m-%d %H:%M:%S')} UTC (spatial bin {spect_loc[0]})")

    # Extract spectrograph data from Data object
    spectra = spect_data.data
    spect_data_timestamps = np.array(spect_data.timestamp)
    metadata = spect_data.metadata
    wavelength = spect_data.metadata[0]['wavelength']

    # Initialize max intensity to zero. This will be used
    # to dynamically determine plotting range
    max_intensity = 0.0

    # Iterate through all requested spectra
    for i in range(len(timestamp)):

        spectra_color = next(color_cycle)

        # Get the spect spatial bin index and timestamp idx
        ts = timestamp[i]
        spect_idx = spect_loc[i]
        epoch_idx = (np.where(spect_data_timestamps == ts))[0]

        # Check for issues with supplied location / time
        if len(epoch_idx) == 0:
            raise ValueError(f"Input does not contain data for requested timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}.")
        if len(epoch_idx) > 1:
            raise ValueError(f"Input contains multiple data points for requested timestamp: {ts.strftime('%Y-%m-%d %H:%M:%S')}.")

        # Get the wavelength array
        wavelength = metadata[epoch_idx[0]]['wavelength']

        # Slice out the spectrum of interest
        spectrum = spectra[:, spect_idx, epoch_idx]

        if ylog:
            spectrum[np.where(spectrum < 0)] = 0

        # Add this spectrum to the plot
        plt.plot(wavelength, spectrum, label=auto_legend[i], color=spectra_color)

        # Update max intensity
        if np.max(spectrum) > max_intensity:
            max_intensity = np.max(spectrum)

    # Add legend if more than one spectrum is plotted
    if auto_legend[0] is not None:
        ax.legend()

    # Set the title
    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title(auto_title)

    # Set x and y labels
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    # Set x-limits, by default to wavelength range
    if xlim is None:
        ax.set_xlim(min(wavelength), max(wavelength))
    else:
        ax.set_xlim(xlim)

    # Set y-limit, by default 1.2 times max spectrum data
    if ylim is None:
        if ylog:
            ax.set_ylim(1.0, max_intensity * 2.0)
        else:
            ax.set_ylim(0.0, max_intensity * 1.2)
    else:
        ax.set_ylim(ylim)

    if ylog:
        ax.set_yscale('log', base=10)

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
                show_warning("The savefig_quality parameter was specified, but is only used for saving JPG files. The " +
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
