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

from wordcab.client import Client
from wordcab.core_objects import BaseTranscript, ListTranscripts


def test_list_transcripts(api_key: str) -> None:
    """Test client list_transcripts method."""
    with Client(api_key=api_key) as client:
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


def test_list_transcripts_page_number(api_key: str) -> None:
    """Test client list_transcripts method with page number."""
    with Client(api_key=api_key) as client:
        nb = 2
        list_transcripts = client.list_transcripts(page_number=nb)
        assert list_transcripts is not None
        assert isinstance(list_transcripts, ListTranscripts)
        assert list_transcripts.page_count is not None
        assert isinstance(list_transcripts.page_count, int)
        assert list_transcripts.next_page is not None
        assert isinstance(list_transcripts.next_page, str)
        assert (
            list_transcripts.next_page
            == f"https://wordcab.com/api/v1/transcripts?page={nb + 1}"
        )
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
