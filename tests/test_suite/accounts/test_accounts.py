from aurorax.exceptions import AuroraXUnauthorizedException
import aurorax
import os
import pytest

ACCOUNTS_URL = "/api/v1/accounts"
aurorax.api.set_base_url("https://api.staging.aurorax.space")

def test_get_all_accounts():
    aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.base_url + ACCOUNTS_URL)
    res = req.execute()
    
    assert type(res.data) is list and len(res.data) > 0
