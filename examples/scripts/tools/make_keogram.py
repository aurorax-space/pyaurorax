import datetime
import matplotlib.pyplot as plt
import numpy as np
import pyaurorax

# init
aurorax = pyaurorax.PyAuroraX()

# download an hour of Gillam TREx RGB data
dataset_name = "TREX_RGB_RAW_NOMINAL"
start_dt = datetime.datetime(2021, 11, 4, 3, 0)
end_dt = datetime.datetime(2021, 11, 4, 3, 59)
r = aurorax.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid="gill", progress_bar_disable=True)

# read in the hour of data
data = aurorax.data.ucalgary.read(r.dataset, r.filenames, n_parallel=5)

# set up working with the tools by just making a shorter name for our future calls
at = aurorax.tools

# scale all the images
#
# NOTE: you can scale all images or just one image
images_scaled = at.scale_intensity(data.data, min=10, max=120)

# make the keogram
keogram = at.keogram.create(images_scaled, data.timestamp)

# show the keogram data
print(keogram)
print(keogram.data)
print(keogram.data.dtype)
