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

"""Test suite for the summary dataclasses."""

import logging
from typing import List

import pytest

from wordcab.core_objects import BaseSummary, ListSummaries, StructuredSummary


logger = logging.getLogger(__name__)


@pytest.fixture
def dummy_structured_summary() -> StructuredSummary:
    """Fixture for a dummy StructuredSummary object."""
    return StructuredSummary(
        end="00:06:49",
        start="00:00:00",
        summary="This is a test.",
        summary_html="<p>This is a test.</p>",
        timestamp_end=409000,
        timestamp_start=0,
    )


@pytest.fixture
def dummy_structured_summary_no_timestamps() -> StructuredSummary:
    """Fixture for a dummy StructuredSummary object without timestamps."""
    return StructuredSummary(
        end_index=10,
        start_index=0,
        summary="This is a test.",
        summary_html="<p>This is a test.</p>",
    )


@pytest.fixture
def dummy_structured_summary_with_context() -> StructuredSummary:
    """Fixture for a dummy StructuredSummary object with context."""
    return StructuredSummary(
        end="00:06:49",
        start="00:00:00",
        summary="This is a test.",
        summary_html="<p>This is a test.</p>",
        timestamp_end=409000,
        timestamp_start=0,
        context={
            "issue": "This is an issue.",
            "purpose": "This is a purpose.",
            "keywords": ["keyword1", "keyword2"],
            "next_steps": {
                "text": "This is a next step.",
                "associated_speakers": ["A", "B"],
            },
            "discussion_points": ["This is a discussion point."],
        },
    )


@pytest.fixture
def dummy_structured_summary_brief_type() -> StructuredSummary:
    """Fixture for a dummy StructuredSummary object with brief summary type."""
    return StructuredSummary(
        end="00:06:49",
        start="00:00:00",
        summary={"title": "This is a test.", "brief_summary": "This is a test."},
        summary_html={
            "title": "<p>This is a test.</p>",
            "brief_summary": "<p>This is a test.</p>",
        },
        timestamp_end=409000,
        timestamp_start=0,
    )


@pytest.fixture
def dummy_empty_base_summary() -> BaseSummary:
    """Fixture for a dummy BaseSummary object."""
    return BaseSummary(
        summary_id="summary_123456",
        job_status="job_status",
        process_time="00:00:00",
    )


@pytest.fixture
def dummy_full_base_summary() -> BaseSummary:
    """Fixture for a dummy BaseSummary object."""
    return BaseSummary(
        summary_id="summary_123456",
        job_status="job_status",
        process_time="00:00:00",
        display_name="display_name",
        job_name="job_name",
        speaker_map={"A": "The Speaker", "B": "The Other Speaker"},
        source="generic",
        source_lang="en",
        summary={
            "test": {
                "structured_summary": [
                    StructuredSummary(
                        summary="test",
                        summary_html="test",
                        start="00:00:00",
                        end="00:00:10",
                        timestamp_start=0,
                        timestamp_end=10,
                    )
                ]
            }
        },
        summary_type="narrative",
        target_lang="en",
        transcript_id="transcript_123456",
        time_started="2021-01-01T00:00:00",
        time_completed="2021-01-01T00:10:00",
    )


@pytest.fixture
def brief_summary() -> BaseSummary:
    """Fixture for a dummy BaseSummary object with a brief summary type."""
    brief_summary = BaseSummary(
        job_status="SummaryComplete",
        summary_id="summary_123456",
        summary_type="brief",
        summary={
            "1": {
                "structured_summary": [
                    StructuredSummary(
                        summary={
                            "title": "This is a title.",
                            "brief_summary": "This is a summary.",
                        }
                    )
                ]
            },
            "3": {
                "structured_summary": [
                    StructuredSummary(
                        summary={
                            "title": "This is a title.",
                            "brief_summary": "This is a summary.",
                        }
                    ),
                    StructuredSummary(
                        summary={
                            "title": "This is another title.",
                            "brief_summary": "This is another summary.",
                        }
                    ),
                ]
            },
            "5": {
                "structured_summary": [
                    StructuredSummary(
                        summary={
                            "title": "This is a title.",
                            "brief_summary": "This is a summary.",
                        }
                    ),
                    StructuredSummary(
                        summary={
                            "title": "This is another title.",
                            "brief_summary": "This is another summary.",
                        }
                    ),
                    StructuredSummary(
                        summary={
                            "title": "This is a third title.",
                            "brief_summary": "This is a third summary.",
                        }
                    ),
                ]
            },
        },
    )

    return brief_summary


@pytest.fixture
def conv_summary() -> BaseSummary:
    """Fixture for a dummy BaseSummary object with a conversation summary type."""
    conv_summary = BaseSummary(
        job_status="SummaryComplete",
        summary_id="summary_123456",
        summary_type="conversational",
        summary={
            "1": {"structured_summary": [StructuredSummary(summary="This is a test.")]},
            "3": {
                "structured_summary": [
                    StructuredSummary(summary="This is a test."),
                    StructuredSummary(summary="This is another test."),
                ]
            },
            "5": {
                "structured_summary": [
                    StructuredSummary(summary="This is a test."),
                    StructuredSummary(summary="This is another test."),
                    StructuredSummary(summary="This is a third test."),
                ]
            },
        },
    )

    return conv_summary


@pytest.fixture
def dummy_list_summaries() -> ListSummaries:
    """Fixture for a dummy ListSummaries object."""
    return ListSummaries(page_count=3, next_page="https://next_page.com", results=[])


def test_empty_structured_summary(
    dummy_structured_summary: StructuredSummary,
) -> None:
    """Test the StructuredSummary object."""
    assert dummy_structured_summary.context is None
    assert dummy_structured_summary.end == "00:06:49"
    assert dummy_structured_summary.start == "00:00:00"
    assert dummy_structured_summary.summary == "This is a test."
    assert dummy_structured_summary.summary_html == "<p>This is a test.</p>"
    assert dummy_structured_summary.timestamp_end == 409000
    assert dummy_structured_summary.timestamp_start == 0
    assert dummy_structured_summary.transcript_segment is None


def test_structured_summary_no_timestamps(
    dummy_structured_summary_no_timestamps: StructuredSummary,
) -> None:
    """Test the StructuredSummary object without timestamps."""
    assert dummy_structured_summary_no_timestamps.context is None
    assert dummy_structured_summary_no_timestamps.end_index == 10
    assert dummy_structured_summary_no_timestamps.start_index == 0
    assert dummy_structured_summary_no_timestamps.summary == "This is a test."
    assert (
        dummy_structured_summary_no_timestamps.summary_html == "<p>This is a test.</p>"
    )
    assert dummy_structured_summary_no_timestamps.transcript_segment is None


def test_structured_summary_with_context(
    dummy_structured_summary_with_context: StructuredSummary,
) -> None:
    """Test the StructuredSummary object with context."""
    assert dummy_structured_summary_with_context.context is not None
    assert isinstance(dummy_structured_summary_with_context.context, dict)
    assert dummy_structured_summary_with_context.context["issue"] == "This is an issue."
    assert (
        dummy_structured_summary_with_context.context["purpose"] == "This is a purpose."
    )
    assert dummy_structured_summary_with_context.context["keywords"] == [
        "keyword1",
        "keyword2",
    ]
    assert dummy_structured_summary_with_context.context["next_steps"] is not None
    assert isinstance(dummy_structured_summary_with_context.context["next_steps"], dict)
    assert dummy_structured_summary_with_context.context["next_steps"][
        "associated_speakers"
    ] == ["A", "B"]
    assert (
        dummy_structured_summary_with_context.context["next_steps"]["text"]
        == "This is a next step."
    )

    assert dummy_structured_summary_with_context.context["discussion_points"] == [
        "This is a discussion point."
    ]


def test_structured_summary_brief_type(
    dummy_structured_summary_brief_type: StructuredSummary,
) -> None:
    """Test the StructuredSummary object with brief summary type."""
    assert dummy_structured_summary_brief_type.context is None
    assert dummy_structured_summary_brief_type.end == "00:06:49"
    assert dummy_structured_summary_brief_type.start == "00:00:00"
    assert dummy_structured_summary_brief_type.summary == {
        "title": "This is a test.",
        "brief_summary": "This is a test.",
    }
    assert dummy_structured_summary_brief_type.summary_html == {
        "title": "<p>This is a test.</p>",
        "brief_summary": "<p>This is a test.</p>",
    }
    assert dummy_structured_summary_brief_type.timestamp_end == 409000
    assert dummy_structured_summary_brief_type.timestamp_start == 0
    assert dummy_structured_summary_brief_type.transcript_segment is None


def test_empty_base_summary(dummy_empty_base_summary: BaseSummary) -> None:
    """Test the empty BaseSummary object."""
    assert dummy_empty_base_summary.summary_id == "summary_123456"
    assert dummy_empty_base_summary.job_status == "job_status"
    assert dummy_empty_base_summary.process_time == "00:00:00"
    assert dummy_empty_base_summary.display_name is None
    assert dummy_empty_base_summary.job_name is None
    assert dummy_empty_base_summary.speaker_map is None
    assert dummy_empty_base_summary.source is None
    assert dummy_empty_base_summary.source_lang is None
    assert dummy_empty_base_summary.summary is None
    assert dummy_empty_base_summary.summary_type is None
    assert dummy_empty_base_summary.target_lang is None
    assert dummy_empty_base_summary.transcript_id is None
    assert dummy_empty_base_summary.time_started is None
    assert dummy_empty_base_summary.time_completed is None


def test_full_base_summary(dummy_full_base_summary: BaseSummary) -> None:
    """Test the full BaseSummary object."""
    assert dummy_full_base_summary.summary_id == "summary_123456"
    assert dummy_full_base_summary.job_status == "job_status"
    assert dummy_full_base_summary.process_time == "00:00:00"
    assert dummy_full_base_summary.display_name == "display_name"
    assert dummy_full_base_summary.job_name == "job_name"
    assert dummy_full_base_summary.speaker_map == {
        "A": "The Speaker",
        "B": "The Other Speaker",
    }
    assert dummy_full_base_summary.source == "generic"
    assert dummy_full_base_summary.source_lang == "en"
    assert dummy_full_base_summary.summary == {
        "test": {
            "structured_summary": [
                StructuredSummary(
                    "test", None, "test", "00:00:10", None, "00:00:00", None, 10, 0
                )
            ]
        }
    }
    assert dummy_full_base_summary.summary_type == "narrative"
    assert dummy_full_base_summary.target_lang == "en"
    assert dummy_full_base_summary.transcript_id == "transcript_123456"
    assert dummy_full_base_summary.time_started == "2021-01-01T00:00:00"
    assert dummy_full_base_summary.time_completed == "2021-01-01T00:10:00"

    assert hasattr(dummy_full_base_summary, "get_summaries") and callable(
        dummy_empty_base_summary.get_summaries
    )
    assert hasattr(dummy_full_base_summary, "get_formatted_summaries") and callable(
        dummy_empty_base_summary.get_formatted_summaries
    )


def test_base_summary_get_summaries(conv_summary: BaseSummary) -> None:
    """Test the BaseSummary object get_summaries method."""
    summaries = conv_summary.get_summaries()

    assert len(summaries) == 3
    assert isinstance(summaries, dict)
    assert summaries["1"] == ["This is a test."]
    assert summaries["3"] == ["This is a test.", "This is another test."]
    assert summaries["5"] == [
        "This is a test.",
        "This is another test.",
        "This is a third test.",
    ]


def test_base_summary_get_summaries_brief(brief_summary: BaseSummary) -> None:
    """Test the BaseSummary object get_summaries method with brief summary type."""
    summaries = brief_summary.get_summaries()

    assert len(summaries) == 3
    assert isinstance(summaries, dict)
    assert summaries["1"] == [["This is a title.", "This is a summary."]]
    assert summaries["3"] == [
        ["This is a title.", "This is a summary."],
        ["This is another title.", "This is another summary."],
    ]
    assert summaries["5"] == [
        ["This is a title.", "This is a summary."],
        ["This is another title.", "This is another summary."],
        ["This is a third title.", "This is a third summary."],
    ]


def test_base_summary_get_formatted_summaries(conv_summary: BaseSummary) -> None:
    """Test the BaseSummary object get_formatted_summaries method."""
    summaries = conv_summary.get_formatted_summaries()

    assert len(summaries) == 3
    assert isinstance(summaries, dict)
    assert summaries["1"] == "conversational - length: 1\n\n[1/1]\nThis is a test.\n\n"
    assert (
        summaries["3"]
        == "conversational - length: 3\n\n[1/2]\nThis is a test.\n\n[2/2]\nThis is another test.\n\n"
    )
    assert (
        summaries["5"] == "conversational - length: 5\n\n"
        "[1/3]\nThis is a test.\n\n[2/3]\nThis is another test.\n\n[3/3]\nThis is a third test.\n\n"
    )


def test_base_summary_get_formatted_summaries_brief(brief_summary: BaseSummary) -> None:
    """Test the BaseSummary object get_formatted_summaries method with brief summary type."""
    summaries = brief_summary.get_formatted_summaries()

    assert len(summaries) == 3
    assert isinstance(summaries, dict)
    assert (
        summaries["1"]
        == "brief - length: 1\n\n[1/1]\nTitle: This is a title.\nSummary: This is a summary.\n\n"
    )
    assert (
        summaries["3"] == "brief - length: 3\n\n"
        "[1/2]\nTitle: This is a title.\nSummary: This is a summary.\n\n"
        "[2/2]\nTitle: This is another title.\nSummary: This is another summary.\n\n"
    )
    assert (
        summaries["5"] == "brief - length: 5\n\n"
        "[1/3]\nTitle: This is a title.\nSummary: This is a summary.\n\n"
        "[2/3]\nTitle: This is another title.\nSummary: This is another summary.\n\n"
        "[3/3]\nTitle: This is a third title.\nSummary: This is a third summary.\n\n"
    )


@pytest.mark.parametrize(
    "params",
    [
        [
            "summary_123456",
            "job_status",
            "narrative",
            "2021-01-01T00:00:00",
            "2021-01-01T00:00:00",
        ],
        [
            "summary_123456",
            "job_status",
            "new_summary_type",
            "2021-01-01T00:00:00",
            "2021-01-01T00:10:00",
        ],
    ],
)
def test_valuerror_base_summary(params: List[str]) -> None:
    """Test the wrong BaseSummary object."""
    with pytest.raises(ValueError):
        BaseSummary(
            summary_id=params[0],
            job_status=params[1],
            summary_type=params[2],
            time_started=params[3],
            time_completed=params[4],
        )


def test_list_summaries(dummy_list_summaries: ListSummaries) -> None:
    """Test the ListSummaries object."""
    assert dummy_list_summaries is not None
    assert dummy_list_summaries.page_count == 3
    assert dummy_list_summaries.next_page == "https://next_page.com"
    assert dummy_list_summaries.results == []
