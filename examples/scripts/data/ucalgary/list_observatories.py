import pyaurorax

aurorax = pyaurorax.PyAuroraX()

observatories = aurorax.data.ucalgary.list_observatories("themis_asi")

print("\nFound %d observatories\n" % (len(observatories)))
for o in observatories:
    print(o)
print()
