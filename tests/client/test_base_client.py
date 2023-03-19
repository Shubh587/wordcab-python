# Copyright 2022-2023 The Wordcab Team. All rights reserved.
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

"""Test suite for the Wordcab Client."""

import pytest

from wordcab import Client


def test_client_succeeds(client: Client) -> None:
    """Test client."""
    assert client.api_key == "dummy_api_key"


def test_client_enter_exit(client: Client) -> None:
    """Test client enter and exit methods."""
    with Client(api_key="dummy_api_key") as client:
        assert client.api_key == "dummy_api_key"


def test_request(client: Client) -> None:
    """Test client request method."""
    with pytest.raises(ValueError):
        client.request(method=None)
