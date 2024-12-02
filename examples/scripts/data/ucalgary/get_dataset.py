import pyaurorax
import pprint

aurorax = pyaurorax.PyAuroraX()

dataset = aurorax.data.get_dataset("THEMIS_ASI_RAW")

print()
print(dataset)
print()

print("Example record in dict format:\n------------------------------\n")
pprint.pprint(dataset.__dict__)
