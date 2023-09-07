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

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import BaseSummary, ListSummaries


class TestListSummaries:
    """Test suite for the Client list_summaries method."""

    summaries = {
        "page_count": 16,
        "next": "https://wordcab.com/api/v1/summaries?page=2",
        "results": [
            {
                "job_status": "SummaryComplete",
                "job_name": "sample_123",
                "transcript_id": "audio_transcript_123",
                "summary_id": "conversational_summary_123",
                "summary_type": "conversational",
                "source": "audio",
                "time_started": "2023-08-30T14:10:22.918254Z",
                "time_completed": "2023-08-30T14:10:50.036129Z",
            },
            {
                "job_status": "Error",
                "summary_id": "conversational_summary_456",
                "time_started": "2023-07-06T12:17:00.506221Z",
            },
            {
                "job_status": "Pending",
                "summary_id": "conversational_summary_789",
                "time_started": "2023-07-06T12:16:51.707461Z",
            },
        ],
    }

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_list_summaries(self, api_key, mock_server) -> None:
        """Test client list_summaries method."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.GET,
                url="https://wordcab.com/api/v1/summaries",
                json=self.summaries,
                status=200,
            )
            list_summaries = client.list_summaries()

            assert list_summaries is not None
            assert isinstance(list_summaries, ListSummaries)

            assert list_summaries.page_count is not None
            assert list_summaries.page_count == self.summaries["page_count"]
            assert isinstance(list_summaries.page_count, int)

            assert list_summaries.next_page is not None
            assert list_summaries.next_page == self.summaries["next"]
            assert isinstance(list_summaries.next_page, str)

            assert list_summaries.results is not None
            assert isinstance(list_summaries.results, list)
            for k_ref, v_ref in self.summaries.items():
                if k_ref == "next":
                    k_ref = "next_page"

                if k_ref == "results":
                    for i, res in enumerate(v_ref):
                        assert getattr(list_summaries, k_ref)[i] == BaseSummary(**res)
                else:
                    assert getattr(list_summaries, k_ref) == v_ref
