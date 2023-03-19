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

"""Test suite for the Client list_jobs method."""

import pytest

from wordcab.client import Client
from wordcab.core_objects import ListJobs


def test_list_jobs(api_key: str) -> None:
    """Test client list_jobs method."""
    with Client(api_key=api_key) as client:
        list_jobs = client.list_jobs()
        assert list_jobs is not None
        assert isinstance(list_jobs, ListJobs)
        assert list_jobs.page_count is not None
        assert isinstance(list_jobs.page_count, int)
        assert list_jobs.next_page is not None
        assert list_jobs.next_page == "https://wordcab.com/api/v1/jobs?page=2"
        assert isinstance(list_jobs.next_page, str)
        assert list_jobs.results is not None
        assert isinstance(list_jobs.results, list)


def test_list_jobs_page_number(api_key: str) -> None:
    """Test client list_jobs method with page number."""
    with Client(api_key=api_key) as client:
        nb = 3
        list_jobs = client.list_jobs(page_number=nb)
        assert list_jobs is not None
        assert isinstance(list_jobs, ListJobs)
        assert list_jobs.page_count is not None
        assert isinstance(list_jobs.page_count, int)
        assert list_jobs.next_page is not None
        assert isinstance(list_jobs.next_page, str)
        assert list_jobs.next_page == f"https://wordcab.com/api/v1/jobs?page={nb + 1}"
        assert list_jobs.results is not None
        assert isinstance(list_jobs.results, list)


def test_error_list_jobs(api_key: str) -> None:
    """Test client list_jobs method with error."""
    with Client(api_key=api_key) as client:
        with pytest.raises(ValueError):
            client.list_jobs(order_by="invalid")
        with pytest.raises(ValueError):
            client.list_jobs(order_by="+time_started")
        with pytest.raises(ValueError):
            client.list_jobs(order_by="+time_completed")
