import pyaurorax
import datetime
import pprint

aurorax = pyaurorax.PyAuroraX()

start_dt = datetime.datetime(2023, 1, 1, 6, 0, 0)
end_dt = datetime.datetime(2023, 1, 1, 6, 9, 59)

print()
res = aurorax.data.ucalgary.download("THEMIS_ASI_RAW", start_dt, end_dt, site_uid="atha", overwrite=True)

print()
print(res)
print()
pprint.pprint(res.__dict__)
print()
