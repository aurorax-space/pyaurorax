import pyaurorax

aurorax = pyaurorax.PyAuroraX()

observatories = aurorax.data.ucalgary.list_observatories("themis_asi", uid="fs")

print("\nFound %d observatories matching the uid filter\n" % (len(observatories)))
for o in observatories:
    print(o)
print()
