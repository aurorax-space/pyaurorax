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


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def host(request):
    return request.config.getoption("--host")


@pytest.fixture(scope="session", autouse=True)
def set_env_api_key(env, host):
    # init
    url = ""
    print(f"\n\nTest environment: {env}")

    # set url and authenticate
    if env == "local":
        url = host
        pyaurorax.api.authenticate(os.getenv("AURORAX_APIKEY_LOCAL"))
    elif env == "staging":
        url = "https://api.staging.aurorax.space"
        pyaurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))
    elif env == "production":
        url = "https://api.aurorax.space"
        pyaurorax.api.authenticate(os.getenv("AURORAX_APIKEY_PRODUCTION"))
    else:
        print(f"Error: env input {env} not recognized")
        sys.exit(-1)

    # check to make sure an API key was set
    if not pyaurorax.get_api_key():
        print(f"Warning: {env} API key not found")

    # set base URL
    print("Using base address: " + url)
    pyaurorax.api.set_base_url(url)
