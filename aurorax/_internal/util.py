import datetime


# json converter
def json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
