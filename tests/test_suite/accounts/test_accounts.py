import pytest
import pyaurorax

ACCOUNTS_URL = "api/v1/accounts"
EXPECTED_ACCOUNT_RECORD_KEYS = [
    "account_id",
    "agree_terms",
    "disabled",
    "email_address",
    "first_name",
    "last_name",
    "role",
]


@pytest.mark.accounts
def test_get_all_accounts():
    """
    Check retrieval of all accounts
    """
    # make request
    url = "%s/%s" % (pyaurorax.api.urls.base_url, ACCOUNTS_URL)
    req = pyaurorax.AuroraXRequest(method="get", url=url)
    res = req.execute()

    # check that there's more than one account returned
    assert type(res.data) is list
    assert len(res.data) > 0

    # check the format of one of the accounts
    account_record = res.data[0]
    account_record_keys = account_record.keys()
    for key in EXPECTED_ACCOUNT_RECORD_KEYS:
        assert key in account_record_keys


@pytest.mark.accounts
@pytest.mark.parametrize("role,expected_min_count",
                         [
                             ("Administrator", 1),
                             ("Owner", 0),
                             ("Maintainer", 0),
                             ("User", 1)
                         ])
def test_get_all_accounts_with_role(role, expected_min_count):
    """
    Check retrieval of all accounts using filtering
    """
    # make request
    url = "%s/%s" % (pyaurorax.api.urls.base_url, ACCOUNTS_URL)
    req = pyaurorax.AuroraXRequest(method="get", url=url, params={"role": role})
    res = req.execute()

    # check to see if there's at least as many as we expect
    assert type(res.data) is list
    assert len(res.data) >= expected_min_count

    # if there's more than one record, check the keys
    if (len(res.data) > 0):
        for account_info in res.data:
            if (account_info["role"] != role):
                assert False
