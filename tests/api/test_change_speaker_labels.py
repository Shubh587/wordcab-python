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

"""Test suite for the API change_speaker_labels function."""

from wordcab.api import change_speaker_labels
from wordcab.core_objects import BaseTranscript


def test_api_change_speaker_labels(api_key: str) -> None:
    """Test the change_speaker_labels function."""
    transcript = change_speaker_labels(
        transcript_id="generic_transcript_JtugR2ELM9u4VSXJmscek7yuKupokH8t",
        speaker_map={"A": "Tom", "B": "Tam", "C": "Tim", "D": "Tum", "E": "Tym"},
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
    assert transcript.speaker_map == {
        "A": "Tom",
        "B": "Tam",
        "C": "Tim",
        "D": "Tum",
        "E": "Tym",
    }
    assert transcript.transcript is not None
    assert isinstance(transcript.transcript, list)
