import os
import pyaurorax
import pytest
import sys


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="staging",
                     choices=["local", "staging", "production"],
                     help="Test server to use. If set to staging or production, "
                     "the corresponding URL for that server will be used. Also the "
                     "environment variable with the corresponding suffix will be used.")
    parser.addoption("--host", action="store", default="http://localhost:3000",
                     help="Local API host address, defaults to localhost:3000 if --env=local")
    parser.addoption("--api-key", type=str,
                     help="A specific API key to use. By default, this is retrieved from "
                     "the environment variable 'AURORAX_APIKEY_STAGING', 'AURORAX_APIKEY_PRODUCTION'"
                     ", or 'AURORAX_APIKEY_LOCAL`")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def host(request):
    return request.config.getoption("--host")


@pytest.fixture(scope="session")
def api_key(request):
    return request.config.getoption("--api-key")


@pytest.fixture(scope="session", autouse=True)
def set_env_api_key(env, host, api_key):
    # init
    url = ""
    print(f"\n\nTest environment: {env}")

    # set url and authenticate
    if (env == "local"):
        url = host
        if (api_key is not None):
            pyaurorax.authenticate(api_key)
        else:
            pyaurorax.authenticate(os.getenv("AURORAX_APIKEY_LOCAL"))
    elif (env == "staging"):
        url = "https://api.staging.aurorax.space"
        if (api_key is not None):
            pyaurorax.authenticate(api_key)
        else:
            pyaurorax.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))
    elif (env == "production"):
        url = "https://api.aurorax.space"
        if (api_key is not None):
            pyaurorax.authenticate(api_key)
        else:
            pyaurorax.authenticate(os.getenv("AURORAX_APIKEY_PRODUCTION"))
    else:
        print(f"Error: env input {env} not recognized")
        sys.exit(-1)

    # check to make sure an API key was set, abort if not found
    if (pyaurorax.get_api_key() == ""):
        print(f"Error: {env} API key not found, aborting tests")
        sys.exit()

    # set base URL
    print("Using base address: " + url)
    pyaurorax.api.set_base_url(url)
