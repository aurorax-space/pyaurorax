import os
import aurorax
import pytest
import sys

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="staging", help="test environment: staging or production")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session", autouse=True)
def set_env_api_key(env):
    if env == "staging":
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))
        aurorax.api.set_base_url("https://api.staging.aurorax.space")
    elif env == "production":
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_PRODUCTION"))
        aurorax.api.set_base_url("https://api.aurorax.space")
    else:
        sys.exit(-1)
