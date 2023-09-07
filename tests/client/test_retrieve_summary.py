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

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import BaseSummary, StructuredSummary


class TestClientRetrieveSummary:
    """Test suite for the Client retrieve_summary method."""

    summary = {
        "job_status": "SummaryComplete",
        "job_name": "job_12345",
        "display_name": "I Love Summarization",
        "summary_id": "narrative_summary_12345",
        "transcript_id": "audio_transcript_12345",
        "summary_type": "narrative",
        "summary": {
            "3": {
                "structured_summary": [
                    {
                        "end": "00:01:47",
                        "start": "00:00:00",
                        "summary": (
                            "SPEAKER A asks SPEAKER B how they can assist them, and"
                            " SPEAKER B notes that they'd like to order flowers."
                            " SPEAKER A asks SPEAKER B their home or office number, and"
                            " SPEAKER B mentions that area code 409-866-5088. SPEAKER A"
                            " asks SPEAKER B their shipping address, and SPEAKER B says"
                            " 6800 avenue, beaumont, texas. SPEAKER A talks about how"
                            " SPEAKER B is ordering one dozen long stands red roses,"
                            " and it will be shipped to their address within 24 hours."
                        ),
                        "summary_html": (
                            '<span class="speaker_a">SPEAKER A</span> asks <span'
                            ' class="speaker_b">SPEAKER B</span> how they can assist'
                            ' them, and <span class="speaker_b">SPEAKER B</span> notes'
                            " that they'd like to order flowers. <span"
                            ' class="speaker_a">SPEAKER A</span> asks <span'
                            ' class="speaker_b">SPEAKER B</span> their home or office'
                            ' number, and <span class="speaker_b">SPEAKER B</span>'
                            " mentions that area code 409-866-5088. <span"
                            ' class="speaker_a">SPEAKER A</span> asks <span'
                            ' class="speaker_b">SPEAKER B</span> their shipping'
                            ' address, and <span class="speaker_b">SPEAKER B</span>'
                            " says 6800 avenue, beaumont, texas. <span"
                            ' class="speaker_a">SPEAKER A</span> talks about how <span'
                            ' class="speaker_b">SPEAKER B</span> is ordering one dozen'
                            " long stands red roses, and it will be shipped to their"
                            " address within 24 hours."
                        ),
                        "timestamp_end": 107740,
                        "timestamp_start": 890,
                        "transcript_segment": [
                            {
                                "end": "00:00:03",
                                "text": (
                                    "Thank you for calling Martha Splurs. How may I"
                                    " assist you?"
                                ),
                                "start": "00:00:00",
                                "speaker": "A",
                                "timestamp_end": 3646,
                                "timestamp_start": 890,
                            },
                            {
                                "end": "00:00:07",
                                "text": (
                                    "Hello. I'd like to order flowers and I think you"
                                    " have what I'm looking for."
                                ),
                                "start": "00:00:03",
                                "speaker": "B",
                                "timestamp_end": 7614,
                                "timestamp_start": 3748,
                            },
                            {
                                "end": "00:00:10",
                                "text": (
                                    "I'll be happy to take care of your order. May I"
                                    " have your name, please?"
                                ),
                                "start": "00:00:07",
                                "speaker": "A",
                                "timestamp_end": 10958,
                                "timestamp_start": 7732,
                            },
                        ],
                    }
                ]
            },
        },
        "speaker_map": {"A": "SPEAKER A", "B": "SPEAKER B"},
        "source": "audio",
        "source_lang": "en",
        "target_lang": "en",
        "time_started": "2023-01-21T10:03:14.906439Z",
        "time_completed": "2023-01-21T10:05:08.021499Z",
    }

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_retrieve_summary(self, api_key, mock_server) -> None:
        """Test client retrieve_summary method."""
        with Client(api_key=api_key) as client:
            summary_id = self.summary["summary_id"]
            mock_server.add(
                responses.GET,
                url=f"https://wordcab.com/api/v1/summaries/{summary_id}",
                json=self.summary,
                status=200,
            )
            summary = client.retrieve_summary(summary_id=summary_id)

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
                assert isinstance(
                    value["structured_summary"][0].transcript_segment, list
                )
                for segment in value["structured_summary"][0].transcript_segment:
                    assert isinstance(segment, dict)
                    assert "speaker" in segment
                    assert "text" in segment
                    assert "timestamp_end" in segment
                    assert "timestamp_start" in segment
                    assert "start" in segment
