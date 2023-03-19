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

"""Test suite for the Client list_summaries method."""

from wordcab.client import Client
from wordcab.core_objects import BaseSummary, ListSummaries


def test_list_summaries(api_key: str) -> None:
    """Test client list_summaries method."""
    with Client(api_key=api_key) as client:
        list_summaries = client.list_summaries()
        assert list_summaries is not None
        assert isinstance(list_summaries, ListSummaries)
        assert list_summaries.page_count is not None
        assert isinstance(list_summaries.page_count, int)
        assert list_summaries.next_page is not None
        assert isinstance(list_summaries.next_page, str)
        assert list_summaries.results is not None
        assert isinstance(list_summaries.results, list)
        for summary in list_summaries.results:
            assert isinstance(summary, BaseSummary)
            assert summary.summary_id is not None
            assert summary.job_status is not None


def test_list_summaries_page_number(api_key: str) -> None:
    """Test client list_summaries method with page number."""
    with Client(api_key=api_key) as client:
        nb = 2
        list_summaries = client.list_summaries(page_number=nb)
        assert list_summaries is not None
        assert isinstance(list_summaries, ListSummaries)
        assert list_summaries.page_count is not None
        assert isinstance(list_summaries.page_count, int)
        assert list_summaries.next_page is not None
        assert isinstance(list_summaries.next_page, str)
        assert (
            list_summaries.next_page
            == f"https://wordcab.com/api/v1/summaries?page={nb + 1}"
        )
        assert list_summaries.results is not None
        assert isinstance(list_summaries.results, list)
        for summary in list_summaries.results:
            assert isinstance(summary, BaseSummary)
            assert summary.summary_id is not None
            assert summary.job_status is not None
