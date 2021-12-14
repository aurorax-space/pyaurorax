import pyaurorax

ACCOUNTS_URL = "/api/v1/accounts"


def test_get_all_accounts():
    req = pyaurorax.AuroraXRequest(
        method="get", url=pyaurorax.api.urls.base_url + ACCOUNTS_URL)
    res = req.execute()

    assert type(res.data) is list and len(res.data) > 0
