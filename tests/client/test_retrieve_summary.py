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

"""Test suite for the Client retrieve_summary method."""

from wordcab.client import Client
from wordcab.core_objects import BaseSummary, StructuredSummary


def test_retrieve_summary(api_key: str) -> None:
    """Test client retrieve_summary method."""
    with Client(api_key=api_key) as client:
        summary = client.retrieve_summary(
            summary_id="narrative_summary_dWmuBMfs4CfKWMn8iGqRwgFmBDHcEx2S"
        )
        assert summary is not None
        assert isinstance(summary, BaseSummary)
        assert summary.summary_id is not None
        assert summary.job_status is not None
        assert summary.job_name is not None
        assert summary.display_name is not None
        assert summary.summary_type is not None
        assert summary.source is not None
        assert summary.source_lang is not None
        assert summary.speaker_map is not None
        assert summary.target_lang is not None
        assert summary.time_started is not None
        assert summary.time_completed is not None
        assert isinstance(summary.summary, dict)
        for key, value in summary.summary.items():
            assert isinstance(key, str)
            assert isinstance(value["structured_summary"][0], StructuredSummary)
            assert value["structured_summary"][0].end is not None
            assert value["structured_summary"][0].start is not None
            assert value["structured_summary"][0].summary is not None
            assert value["structured_summary"][0].summary_html is not None
            assert value["structured_summary"][0].timestamp_end is not None
            assert value["structured_summary"][0].timestamp_start is not None
            assert value["structured_summary"][0].transcript_segment is not None
            assert isinstance(value["structured_summary"][0].transcript_segment, list)
            for segment in value["structured_summary"][0].transcript_segment:
                assert isinstance(segment, dict)
                assert "speaker" in segment
                assert "text" in segment
                assert "timestamp_end" in segment
                assert "timestamp_start" in segment
                assert "start" in segment
