import pyaurorax
import datetime
import glob

# init
aurorax = pyaurorax.PyAuroraX()

# set list of files (we could do this using a glob too)
file_list = sorted(glob.glob("/mnt/ceph/trex/rgb/unstable/stream0/2023/01/01/atha*/ut06/*_060[0,1,2]_*.pgm*"))

# read data
print("\n[%s] Reading data ..." % (datetime.datetime.now()))
data = aurorax.data.ucalgary.readers.read_trex_rgb(file_list, n_parallel=2)

print()
print(data)
