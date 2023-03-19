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

"""Test suite for the API retrieve_transcript function."""

from wordcab.api import retrieve_transcript
from wordcab.core_objects import BaseTranscript, TranscriptUtterance


def test_api_retrieve_transcript(api_key: str) -> None:
    """Test the retrieve_transcript function."""
    transcript = retrieve_transcript(
        transcript_id="generic_transcript_JU74t3Tjzahn5DodBLwsDrS2EvGdb4bS",
        api_key=api_key,
    )
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
