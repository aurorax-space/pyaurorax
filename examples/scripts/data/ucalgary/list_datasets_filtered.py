import pyaurorax
import pprint

aurorax = pyaurorax.PyAuroraX()

datasets = aurorax.data.ucalgary.list_datasets(name="REGO_CALIBRATION")

print("\nFound %d datasets matching the name filter\n------------------------------\n" % (len(datasets)))
pprint.pprint(datasets)

print("\nExample record in dict format:\n------------------------------\n")
pprint.pprint(datasets[0].__dict__)
print()
