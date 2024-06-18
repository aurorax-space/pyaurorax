import datetime
import pyaurorax

aurorax = pyaurorax.PyAuroraX()

output = pyaurorax.models.ATMInverseOutputFlags()
output.set_all_true()
# output.energy_flux = True
# output.characteristic_energy = True
# output.oxygen_correction_factor = True
# output.altitudes = True
# output.emission_5577 = True

timestamp = datetime.datetime(2022, 1, 1, 6, 0, 0)
lat = 51.04
lon = -100.0
intensity_4278 = 2302.6
intensity_5577 = 11339.5
intensity_6300 = 528.3
intensity_8446 = 427.4

result = aurorax.models.atm.inverse(timestamp, lat, lon, intensity_4278, intensity_5577, intensity_6300, intensity_8446, output)

print()
print(result)
print()
result.pretty_print()
print()
