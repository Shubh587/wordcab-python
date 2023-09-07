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

"""Test suite for the Client retrieve_transcript method."""

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import BaseTranscript, TranscriptUtterance


class TestClientRetrieveTranscript:
    """Test suite for the Client retrieve_transcript method."""

    transcript = {
        "transcript_id": "generic_transcript_12345",
        "job_id_set": ["job_12345"],
        "summary_id_set": ["conversational_summary_12345"],
        "transcript": [
            {
                "end": "00:00:06",
                "text": (
                    "Thank you for calling the Concierge department. My name is John"
                    " Doe. With whom do I have the pleasure of speaking with today?"
                ),
                "start": "00:00:00",
                "speaker": "A",
                "timestamp_end": 6000,
                "timestamp_start": 0,
            },
            {
                "end": "00:00:30",
                "text": (
                    "Yes, this is speaking. I have reservations for the 911 Memorial"
                    " Museum tomorrow at 01:00 and I'm wondering if I could change that"
                    " to 11:00. I called them and they don't have a record of my"
                    " tickets."
                ),
                "start": "00:00:06",
                "speaker": "B",
                "timestamp_end": 30000,
                "timestamp_start": 6000,
            },
            {
                "end": "00:00:45",
                "text": (
                    "Okay, so let me go ahead and see if I can call them directly and"
                    " check if I can change the time for you before that. This phone"
                    " number that you're calling from, which is Jane Doe, is that the"
                    " number associated with your account?"
                ),
                "start": "00:00:31",
                "speaker": "A",
                "timestamp_end": 45000,
                "timestamp_start": 31000,
            },
        ],
        "speaker_map": {
            "A": "SPEAKER A",
            "B": "SPEAKER B",
        },
    }

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_retrieve_transcript(self, api_key, mock_server) -> None:
        """Test client retrieve_transcript method."""
        with Client(api_key=api_key) as client:
            transcript_id = self.transcript["transcript_id"]
            mock_server.add(
                responses.GET,
                url=f"https://wordcab.com/api/v1/transcripts/{transcript_id}",
                json=self.transcript,
                status=200,
            )
            transcript = client.retrieve_transcript(transcript_id=transcript_id)

            assert transcript is not None
            assert isinstance(transcript, BaseTranscript)
            assert transcript.transcript_id is not None
            assert isinstance(transcript.transcript_id, str)
            assert transcript.job_id_set is not None
            assert isinstance(transcript.job_id_set, list)
            assert transcript.summary_id_set is not None
            assert isinstance(transcript.summary_id_set, list)
            assert transcript.speaker_map is not None
            assert isinstance(transcript.speaker_map, dict)
            assert transcript.transcript is not None
            assert isinstance(transcript.transcript, list)
            for utterance in transcript.transcript:
                assert isinstance(utterance, TranscriptUtterance)
                assert utterance.end is not None
                assert isinstance(utterance.end, str)
                assert utterance.start is not None
                assert isinstance(utterance.start, str)
                assert utterance.speaker is not None
                assert isinstance(utterance.speaker, str)
                assert utterance.text is not None
                assert isinstance(utterance.text, str)
                assert utterance.timestamp_end is not None
                assert isinstance(utterance.timestamp_end, int)
                assert utterance.timestamp_start is not None
                assert isinstance(utterance.timestamp_start, int)
