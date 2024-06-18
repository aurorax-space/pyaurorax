import datetime
import pyaurorax

aurorax = pyaurorax.PyAuroraX()

output = pyaurorax.models.ATMForwardOutputFlags()
output.enable_only_height_integrated_rayleighs()
output.altitudes = True
output.emission_5577 = True
timestamp = datetime.datetime.now().replace(hour=6, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)

result = aurorax.models.atm.forward(timestamp, 51.04, -114.5, output)

print()
print(result)
print()
result.pretty_print()
print()
