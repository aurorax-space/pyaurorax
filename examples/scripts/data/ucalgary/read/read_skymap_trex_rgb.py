import pyaurorax
import datetime
import pprint

# init
aurorax = pyaurorax.PyAuroraX()

# get dataset
print("\n[%s] Getting dataset ..." % (datetime.datetime.now()))
dataset = aurorax.data.ucalgary.list_datasets("TREX_RGB_SKYMAP_IDLSAV")[0]

# download data
print("\n[%s] Downloading data ..." % (datetime.datetime.now()))
start_dt = datetime.datetime(2022, 1, 1, 0, 0, 0)
end_dt = datetime.datetime(2022, 12, 31, 23, 59, 59)
site_uid = "luck"
download_obj = aurorax.data.ucalgary.download(dataset.name, start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)

# set list of files (we could do this using a glob too)
file_list = download_obj.filenames

# read data
print("\n[%s] Reading data ..." % (datetime.datetime.now()))
data = aurorax.data.ucalgary.read(dataset, file_list, n_parallel=2)

print()
print(data.data[0])
print()
