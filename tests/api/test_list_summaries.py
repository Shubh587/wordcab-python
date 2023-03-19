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

"""Test suite for the API list_summaries function."""

from wordcab.api import list_summaries
from wordcab.core_objects import BaseSummary, ListSummaries


def test_api_list_summaries(api_key: str) -> None:
    """Test the list_summaries function."""
    li_summaries = list_summaries(api_key=api_key)
    assert li_summaries is not None
    assert isinstance(li_summaries, ListSummaries)
    assert li_summaries.page_count is not None
    assert isinstance(li_summaries.page_count, int)
    assert li_summaries.next_page is not None
    assert isinstance(li_summaries.next_page, str)
    assert li_summaries.results is not None
    assert isinstance(li_summaries.results, list)
    for summary in li_summaries.results:
        assert isinstance(summary, BaseSummary)
        assert summary.summary_id is not None
        assert summary.job_status is not None


def test_list_summaries_page_number(api_key: str) -> None:
    """Test the list_summaries function with page number."""
    nb = 3
    li_summaries = list_summaries(page_number=nb, api_key=api_key)
    assert li_summaries is not None
    assert isinstance(li_summaries, ListSummaries)
    assert li_summaries.page_count is not None
    assert isinstance(li_summaries.page_count, int)
    assert li_summaries.next_page is not None
    assert isinstance(li_summaries.next_page, str)
    assert (
        li_summaries.next_page == f"https://wordcab.com/api/v1/summaries?page={nb + 1}"
    )
    assert li_summaries.results is not None
    assert isinstance(li_summaries.results, list)
    for summary in li_summaries.results:
        assert isinstance(summary, BaseSummary)
        assert summary.summary_id is not None
        assert summary.job_status is not None
