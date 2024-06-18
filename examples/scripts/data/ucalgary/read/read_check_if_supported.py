import pyaurorax

# init
aurorax = pyaurorax.PyAuroraX()

# check
print()
print("THEMIS_ASI_RAW supported: %s" % (aurorax.data.ucalgary.is_read_supported("THEMIS_ASI_RAW")))
print("SOME_BAD_DATASET supported: %s" % (aurorax.data.ucalgary.is_read_supported("THEMIS_SOME_BAD_DATASETASI_RAW")))
print()
