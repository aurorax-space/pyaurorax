import pyaurorax
import datetime

# init
aurorax = pyaurorax.PyAuroraX()

# get dataset
print("\n[%s] Getting dataset ..." % (datetime.datetime.now()))
dataset = aurorax.data.ucalgary.get_dataset("TREX_SPECT_PROCESSED_V1")

# download data
print("\n[%s] Downloading data ..." % (datetime.datetime.now()))
start_dt = datetime.datetime(2018, 2, 10, 6, 0, 0)
end_dt = datetime.datetime(2018, 2, 10, 6, 59, 59)
site_uid = "luck"
download_obj = aurorax.data.ucalgary.download(dataset.name, start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)

# set list of files (we could do this using a glob too)
file_list = download_obj.filenames

# read data
print("\n[%s] Reading data ..." % (datetime.datetime.now()))
data = aurorax.data.ucalgary.readers.read_trex_spectrograph(file_list, n_parallel=1, dataset=dataset)

print()
print(data)