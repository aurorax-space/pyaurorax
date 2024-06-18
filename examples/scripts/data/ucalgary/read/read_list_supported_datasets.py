import pyaurorax

# init
aurorax = pyaurorax.PyAuroraX()

# get list
datasets = aurorax.data.ucalgary.list_supported_read_datasets()

print()
print(datasets)
