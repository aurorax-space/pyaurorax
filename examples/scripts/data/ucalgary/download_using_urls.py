import pyaurorax
import datetime
import pprint

aurorax = pyaurorax.PyAuroraX()

start_dt = datetime.datetime(2023, 1, 1, 6, 0, 0)
end_dt = datetime.datetime(2023, 1, 1, 6, 9, 59)

# get urls
file_listing_obj = aurorax.data.ucalgary.get_urls("THEMIS_ASI_RAW", start_dt, end_dt, site_uid="atha")

# do fewer urls
file_listing_obj.urls = file_listing_obj.urls[0:2]

# download urls
print()
res = aurorax.data.ucalgary.download_using_urls(file_listing_obj, overwrite=True)

print()
print(res)
print()
pprint.pprint(res.__dict__)
print()
