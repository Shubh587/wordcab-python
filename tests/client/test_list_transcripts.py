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

"""Test suite for the Client list_transcripts method."""

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import BaseTranscript, ListTranscripts


class TestListTranscripts:
    """Test suite for the Client list_transcripts method."""

    transcripts = {
        "page_count": 68,
        "next": "https://wordcab.com/api/v1/transcripts?page=2",
        "results": [
            {
                "transcript_id": "generic_transcript_123",
                "job_id_set": ["job_123"],
                "summary_id_set": ["conversational_summary_123"],
            },
            {
                "transcript_id": "generic_transcript_456",
                "job_id_set": ["job_456"],
                "summary_id_set": ["no_speaker_summary_456"],
            },
            {
                "transcript_id": "generic_transcript_789",
                "job_id_set": [],
                "summary_id_set": ["conversational_summary_789"],
            },
        ],
    }

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_list_transcripts(self, api_key, mock_server) -> None:
        """Test client list_transcripts method."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.GET,
                url="https://wordcab.com/api/v1/transcripts",
                json=self.transcripts,
                status=200,
            )
            list_transcripts = client.list_transcripts()

            assert list_transcripts is not None
            assert isinstance(list_transcripts, ListTranscripts)

            assert list_transcripts.page_count is not None
            assert isinstance(list_transcripts.page_count, int)

            assert list_transcripts.next_page is not None
            assert isinstance(list_transcripts.next_page, str)

            assert list_transcripts.results is not None
            assert isinstance(list_transcripts.results, list)

            for transcript in list_transcripts.results:
                assert isinstance(transcript, BaseTranscript)
                assert transcript.transcript_id is not None
                assert isinstance(transcript.transcript_id, str)
                assert transcript.job_id_set is not None
                assert isinstance(transcript.job_id_set, list)
                assert transcript.summary_id_set is not None
                assert isinstance(transcript.summary_id_set, list)
