# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

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


@pytest.mark.search_ro
def test_get_all_accounts(aurorax):
    """
    Check retrieval of all accounts
    """
    # make request
    url = "%s/%s" % (aurorax.api_base_url, ACCOUNTS_URL)
    req = aurorax.search.api.AuroraXAPIRequest(aurorax, method="get", url=url)
    res = req.execute()

    # check that there's more than one account returned
    assert isinstance(res.data, list) is True
    assert len(res.data) > 0

    # check the format of one of the accounts
    account_record = res.data[0]
    account_record_keys = account_record.keys()
    for key in EXPECTED_ACCOUNT_RECORD_KEYS:
        assert key in account_record_keys


@pytest.mark.search_ro
@pytest.mark.parametrize("role,expected_min_count", [
    ("Administrator", 1),
    ("Owner", 0),
    ("Maintainer", 0),
    ("User", 1),
])
def test_get_all_accounts_with_role(aurorax, role, expected_min_count):
    """
    Check retrieval of all accounts using filtering
    """
    # make request
    url = "%s/%s" % (aurorax.api_base_url, ACCOUNTS_URL)
    req = aurorax.search.api.AuroraXAPIRequest(aurorax, method="get", url=url, params={"role": role})
    res = req.execute()

    # check to see if there's at least as many as we expect
    assert isinstance(res.data, list) is True
    assert len(res.data) >= expected_min_count

    # if there's more than one record, check the keys
    if (len(res.data) > 0):
        for account_info in res.data:
            assert account_info["role"] == role
