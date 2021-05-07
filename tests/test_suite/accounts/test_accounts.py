from aurorax.exceptions import AuroraXUnauthorizedException
import aurorax
import pytest

ACCOUNTS_URL = "/api/v1/accounts"

def test_get_all_accounts():
    api_key = "ff179c25-962f-4cc8-b77d-bf16768c0991:c2c008f9-c50f-445c-a459-982606e0b1b1"
    aurorax.api.set_base_url("https://api.staging.aurorax.space")
    aurorax.authenticate(api_key)

    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.base_url + ACCOUNTS_URL)
    res = req.execute()

    assert res.data is list and len(res.data) > 0


def test_bad_api_key():
    with pytest.raises(AuroraXUnauthorizedException):
        api_key = "ff179c25-962f-4cc8-b77d-bf16768c0991:c2c008f9-c50f-445c-a459-982606e0b1b"
        aurorax.api.set_base_url("https://api.staging.aurorax.space")
        aurorax.authenticate(api_key)

        req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.base_url + ACCOUNTS_URL)
            
        res = req.execute()
