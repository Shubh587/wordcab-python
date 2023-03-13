# Copyright 2023 The Wordcab Team. All rights reserved.
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

"""Test suite for the config.py file."""

from pathlib import Path

from wordcab.config import (
    AVAILABLE_AUDIO_FORMATS,
    AVAILABLE_GENERIC_FORMATS,
    AVAILABLE_PLAN,
    CONTEXT_ELEMENTS,
    EXTRACT_AVAILABLE_STATUS,
    EXTRACT_PIPELINES,
    LIST_JOBS_ORDER_BY,
    REQUEST_TIMEOUT,
    SOURCE_LANG,
    SOURCE_OBJECT_MAPPING,
    SUMMARIZE_AVAILABLE_STATUS,
    SUMMARY_LENGTHS_RANGE,
    SUMMARY_PIPELINES,
    SUMMARY_TYPES,
    TARGET_LANG,
    WORDCAB_TOKEN_FOLDER,
)


def test_available_audio_formats() -> None:
    """Test the AVAILABLE_AUDIO_FORMATS constant."""
    assert isinstance(AVAILABLE_AUDIO_FORMATS, list)
    assert len(AVAILABLE_AUDIO_FORMATS) > 0
    assert all(isinstance(item, str) for item in AVAILABLE_AUDIO_FORMATS)
    assert all(item.startswith(".") for item in AVAILABLE_AUDIO_FORMATS)
    assert all(item.lower() == item for item in AVAILABLE_AUDIO_FORMATS)
    assert AVAILABLE_AUDIO_FORMATS == [".flac", ".m4a", ".mp3", ".mpga", ".ogg", ".wav"]


def test_available_generic_formats() -> None:
    """Test the AVAILABLE_GENERIC_FORMATS constant."""
    assert isinstance(AVAILABLE_GENERIC_FORMATS, list)
    assert len(AVAILABLE_GENERIC_FORMATS) > 0
    assert all(isinstance(item, str) for item in AVAILABLE_GENERIC_FORMATS)
    assert all(item.startswith(".") for item in AVAILABLE_GENERIC_FORMATS)
    assert all(item.lower() == item for item in AVAILABLE_GENERIC_FORMATS)
    assert AVAILABLE_GENERIC_FORMATS == [".json", ".txt"]


def test_available_plan() -> None:
    """Test the AVAILABLE_PLAN constant."""
    assert isinstance(AVAILABLE_PLAN, list)
    assert len(AVAILABLE_PLAN) > 0
    assert all(isinstance(item, str) for item in AVAILABLE_PLAN)
    assert AVAILABLE_PLAN == ["free", "metered", "paid"]


def test_context_elements() -> None:
    """Test the CONTEXT_ELEMENTS constant."""
    assert isinstance(CONTEXT_ELEMENTS, list)
    assert len(CONTEXT_ELEMENTS) > 0
    assert all(isinstance(item, str) for item in CONTEXT_ELEMENTS)
    assert CONTEXT_ELEMENTS == [
        "discussion_points",
        "issue",
        "keywords",
        "next_steps",
        "purpose",
    ]


def test_extract_available_status() -> None:
    """Test the EXTRACT_AVAILABLE_STATUS constant."""
    assert isinstance(EXTRACT_AVAILABLE_STATUS, list)
    assert len(EXTRACT_AVAILABLE_STATUS) > 0
    assert all(isinstance(item, str) for item in EXTRACT_AVAILABLE_STATUS)
    assert EXTRACT_AVAILABLE_STATUS == [
        "Deleted",
        "Error",
        "Extracting",
        "ExtractionComplete",
        "ItemQueued",
        "Pending",
        "PreparingExtraction",
    ]


def test_extract_pipelines() -> None:
    """Test the EXTRACT_PIPELINES constant."""
    assert isinstance(EXTRACT_PIPELINES, list)
    assert len(EXTRACT_PIPELINES) > 0
    assert all(isinstance(item, str) for item in EXTRACT_PIPELINES)
    assert EXTRACT_PIPELINES == [
        "questions_answers",
        "topic_segments",
        "emotions",
        "speaker_talk_ratios",
    ]


def test_list_jobs_order_by() -> None:
    """Test the LIST_JOBS_ORDER_BY constant."""
    assert isinstance(LIST_JOBS_ORDER_BY, list)
    assert len(LIST_JOBS_ORDER_BY) > 0
    assert all(isinstance(item, str) for item in LIST_JOBS_ORDER_BY)
    assert LIST_JOBS_ORDER_BY == [
        "time_started",
        "time_completed",
        "-time_started",
        "-time_completed",
    ]


def test_request_timeout() -> None:
    """Test the REQUEST_TIMEOUT constant."""
    assert isinstance(REQUEST_TIMEOUT, int)
    assert REQUEST_TIMEOUT > 0
    assert REQUEST_TIMEOUT == 30


def test_source_lang() -> None:
    """Test the SOURCE_LANG constant."""
    assert isinstance(SOURCE_LANG, list)
    assert len(SOURCE_LANG) > 0
    assert all(isinstance(item, str) for item in SOURCE_LANG)
    assert SOURCE_LANG == ["de", "en", "es", "fr", "it", "pt", "sv"]


def test_source_object_mapping() -> None:
    """Test the SOURCE_OBJECT_MAPPING constant."""
    assert isinstance(SOURCE_OBJECT_MAPPING, dict)
    assert len(SOURCE_OBJECT_MAPPING) > 0
    assert all(isinstance(key, str) for key in SOURCE_OBJECT_MAPPING.keys())
    assert all(isinstance(value, str) for value in SOURCE_OBJECT_MAPPING.values())
    assert SOURCE_OBJECT_MAPPING == {
        "generic": "GenericSource",
        "audio": "AudioSource",
        "wordcab_transcript": "WordcabTranscriptSource",
        "signed_url": "SignedUrlSource",
        "assembly_ai": "AssemblyAISource",
        "deepgram": "DeepgramSource",
        "rev_ai": "RevSource",
        "vtt": "VTTSource",
    }


def test_summarize_available_status() -> None:
    """Test the SUMMARIZE_AVAILABLE_STATUS constant."""
    assert isinstance(SUMMARIZE_AVAILABLE_STATUS, list)
    assert len(SUMMARIZE_AVAILABLE_STATUS) > 0
    assert all(isinstance(item, str) for item in SUMMARIZE_AVAILABLE_STATUS)
    assert SUMMARIZE_AVAILABLE_STATUS == [
        "Deleted",
        "Error",
        "ItemQueued",
        "Pending",
        "PreparingSummary",
        "PreparingTranscript",
        "Summarizing",
        "SummaryComplete",
        "Transcribing",
        "TranscriptComplete",
    ]


def test_summary_lengths_range() -> None:
    """Test the SUMMARY_LENGTHS_RANGE constant."""
    assert isinstance(SUMMARY_LENGTHS_RANGE, list)
    assert len(SUMMARY_LENGTHS_RANGE) == 2
    assert all(isinstance(item, int) for item in SUMMARY_LENGTHS_RANGE)
    assert SUMMARY_LENGTHS_RANGE == [1, 5]


def test_summary_pipelines() -> None:
    """Test the SUMMARY_PIPELINES constant."""
    assert isinstance(SUMMARY_PIPELINES, list)
    assert len(SUMMARY_PIPELINES) > 0
    assert all(isinstance(item, str) for item in SUMMARY_PIPELINES)
    assert SUMMARY_PIPELINES == ["transcribe", "summarize"]


def test_summary_types() -> None:
    """Test the SUMMARY_TYPES constant."""
    assert isinstance(SUMMARY_TYPES, list)
    assert len(SUMMARY_TYPES) > 0
    assert all(isinstance(item, str) for item in SUMMARY_TYPES)
    assert SUMMARY_TYPES == ["conversational", "narrative", "no_speaker"]


def test_target_lang() -> None:
    """Test the TARGET_LANG constant."""
    assert isinstance(TARGET_LANG, list)
    assert len(TARGET_LANG) > 0
    assert all(isinstance(item, str) for item in TARGET_LANG)
    assert TARGET_LANG == ["de", "en", "es", "fr", "it", "pt", "sv"]


def test_wordcab_token_folder() -> None:
    """Test the WORDCAB_TOKEN_FOLDER constant."""
    assert isinstance(WORDCAB_TOKEN_FOLDER, Path)
    full_path = Path.home() / ".wordcab" / "token"
    assert WORDCAB_TOKEN_FOLDER == full_path
