import os
import sys
import json
import requests
import datetime
sys.path.append(".")

from aurorax import ephemeris, conjunctions

def test_ephemeris_sources():
    # get all ephemeris sources
    print("\nTest: getting ephemeris sources")
    
    try:
        ax = ephemeris.get_ephemeris_sources()
        #return True
    
        if len(ax) > 0:
            print("Successfully got ephemeris sources")
            return True
        
    except Exception as e:
        print("--- An exception occurred while testing getting ephemeris sources:")
        print(e)
        
    return False


def test_ephemeris_search():
    # send search request for a single record
    print("\nTest: searching ephemeris records")
    
    try:
        start = datetime.datetime(2019, 2, 5, 0, 0, 0)
        end = datetime.datetime(2019, 2, 5, 0, 10, 0)
        program = ["swarm"]
        platform = ["swarma"]
        instrument_type = ["ssc-web"]

        ax = ephemeris.EphemerisSearch(start=start, end=end, programs=program, platforms=platform, instrument_types=instrument_type)
        result = ax.execute()
        #result = [True]
        
        if result == -1 or result == []:
            return False
        
        return True
    
    except Exception as e:
        print("--- An exception occurred while testing ephemeris search:")
        print(e)

    return False


def test_simple_conjunction():
    print("\nTest: simple conjunction search")
    
    try:
        start = datetime.datetime(2019, 2, 5, 0, 0, 0)
        end = datetime.datetime(2019, 2, 10, 23, 59, 59)
        
        cs = conjunctions.ConjunctionSearch()
        cs.start = start
        cs.end = end
        cs.add_ground(programs=["themis-asi"])
        cs.add_space(programs=["swarm"], instrument_types=["ssc-web"])
        
        result = cs.execute()
        #result = [True]
        
        if result == -1 or result == []:
            return False
        
        return True
    
    except Exception as e:
        print("--- An exception occurred while testing simple conjunction search:")
        print(e)
        
    return False
        
    
def main():
    print("Running tests at " + sys.argv[0])
    
    failures = False
    
    for test in [test_ephemeris_sources, test_ephemeris_search, test_simple_conjunction]:
        if not test():
            print("\n--- Failed test! Aborting remaining test(s)")
            failures = True
            break
        
        print("Test passed.")
        
    if failures:
        print("--- Tests aborted with failures.\n")
    else:
        print("--- All tests passed.\n")

    return

if __name__ == "__main__":
    main()