import aurorax

ACCOUNTS_URL = "/api/v1/accounts"

def test_get_all_accounts():
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.base_url + ACCOUNTS_URL)
    res = req.execute()
    
    assert type(res.data) is list and len(res.data) > 0
