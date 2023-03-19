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

"""Test suite for the API list_jobs function."""

import pytest

from wordcab.api import list_jobs
from wordcab.core_objects import ListJobs


def test_api_list_jobs(api_key: str) -> None:
    """Test the list_jobs function."""
    jobs = list_jobs(api_key=api_key)
    assert jobs is not None
    assert isinstance(jobs, ListJobs)
    assert jobs.page_count is not None
    assert isinstance(jobs.page_count, int)
    assert jobs.next_page is not None
    assert isinstance(jobs.next_page, str)
    assert jobs.results is not None
    assert isinstance(jobs.results, list)


def test_list_jobs_page_number(api_key: str) -> None:
    """Test the list_jobs function with a page number."""
    nb = 3
    jobs = list_jobs(page_number=nb, api_key=api_key)
    assert jobs is not None
    assert isinstance(jobs, ListJobs)
    assert jobs.page_count is not None
    assert isinstance(jobs.page_count, int)
    assert jobs.next_page is not None
    assert isinstance(jobs.next_page, str)
    assert jobs.next_page == f"https://wordcab.com/api/v1/jobs?page={nb + 1}"
    assert jobs.results is not None
    assert isinstance(jobs.results, list)


def test_error_list_jobs() -> None:
    """Test the list_jobs function with an invalid API key."""
    with pytest.raises(ValueError):
        list_jobs(order_by="invalid")
    with pytest.raises(ValueError):
        list_jobs(order_by="+time_started")
    with pytest.raises(ValueError):
        list_jobs(order_by="+time_completed")
