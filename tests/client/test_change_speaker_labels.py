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

"""Test suite for the Client change_speaker_labels method."""

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import BaseTranscript


class TestClientChangeSpeakerLabels:
    """Test suite for the Client change_speaker_labels method."""

    @pytest.mark.usefixtures("api_key", "get_transcript_id", "mock_server")
    def test_change_speaker_labels(
        self, api_key, get_transcript_id, mock_server
    ) -> None:
        """Test client change_speaker_labels method."""
        speaker_map = {"A": "Tam", "B": "Tim", "C": "Tom", "D": "Tum", "E": "Tym"}

        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.PATCH,
                f"https://wordcab.com/api/v1/transcripts/{get_transcript_id}",
                json={"transcript_id": get_transcript_id, "speaker_map": speaker_map},
                status=200,
            )
            transcript = client.change_speaker_labels(
                transcript_id=get_transcript_id,
                speaker_map=speaker_map,
            )
            assert transcript is not None
            assert isinstance(transcript, BaseTranscript)

            assert transcript.transcript_id is not None
            assert transcript.transcript_id == get_transcript_id
            assert isinstance(transcript.transcript_id, str)

            assert transcript.job_id_set is not None
            assert isinstance(transcript.job_id_set, list)

            assert transcript.summary_id_set is not None
            assert isinstance(transcript.summary_id_set, list)

            assert transcript.speaker_map is not None
            assert transcript.speaker_map == speaker_map
            assert isinstance(transcript.speaker_map, dict)

            assert transcript.transcript is not None
            assert isinstance(transcript.transcript, list)
