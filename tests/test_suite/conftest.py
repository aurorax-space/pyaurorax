import os
import aurorax
import pytest
import sys


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="staging",
                     help="Test environment: 'local', 'staging', or 'production'. Defaults to 'staging'.")
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
    url = ""
    print(f"\n\nTest environment: {env}")

    if env == "local":
        url = host
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_LOCAL"))
    elif env == "staging":
        url = "https://api.staging.aurorax.space"
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))
    elif env == "production":
        url = "https://api.aurorax.space"
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_PRODUCTION"))
    else:
        print(f"Error: env input {env} not recognized")
        sys.exit(-1)

    if not aurorax.get_api_key():
        print(f"Warning: {env} API key not found")

    print("Using base address: " + url)
    aurorax.api.set_base_url(url)
