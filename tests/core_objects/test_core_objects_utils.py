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

"""Test suite for the core objects utils functions."""

import textwrap
from typing import Any, Dict, List, Union

import pytest
from wordcab.core_objects.utils import (
    _get_assembly_utterances,
    _get_context_items,
    _get_deepgram_utterances,
    _get_rev_monologues,
    _textwrap,
)


def test_textwrap_default_width() -> None:
    """Test that _textwrap wraps the text to the default width of 80."""
    text_to_wrap = (
        "This is a long text that should be wrapped to the specified width of 80"
        " characters by default."
    )

    expected_result = "\n".join(textwrap.wrap(text_to_wrap, width=80))
    result = _textwrap(text_to_wrap)

    assert result == expected_result
    assert len(result) == len(expected_result)


def test_textwrap_custom_width() -> None:
    """Test that _textwrap wraps the text to the specified custom width."""
    text_to_wrap = "This is a long text that should be wrapped to a custom width."
    width = 30

    expected_result = "\n".join(textwrap.wrap(text_to_wrap, width=width))
    result = _textwrap(text_to_wrap, width=width)

    assert result == expected_result
    assert len(result) == len(expected_result)


def test_issue_in_context() -> None:
    """Test that _get_context_items includes 'Issue' when it is in the context."""
    context = {"issue": "This is an issue"}

    result = _get_context_items(context)

    assert "Issue: This is an issue\n" == result


def test_multiple_context_items() -> None:
    """Test that _get_context_items includes all context items."""
    context = {
        "issue": "This is an issue",
        "purpose": "This is a purpose",
        "next_steps": {
            "text": "These are next steps",
            "associated_speakers": ["SPEAKER B"],
        },
        "discussion_points": [
            "These are discussion points",
            "These are more discussion points",
        ],
        "keywords": ["These are keywords", "These are more keywords"],
    }

    result = _get_context_items(context)

    expected_result = (
        "Issue: This is an issue\nPurpose: This is a purpose\nNext steps: {'text':"
        " 'These are next steps', 'associated_speakers': ['SPEAKER B']}\nDiscussion"
        " points: ['These are discussion points', 'These are more discussion"
        " points']\nKeywords: ['These are keywords', 'These are more keywords']\n"
    )
    assert expected_result == result


def test_no_context_items() -> None:
    """Test that _get_context_items returns an empty string when there are no context items."""
    context: Dict[str, Any] = {}

    result = _get_context_items(context)

    assert "" == result


def test_get_assembly_utterances_valid() -> None:
    """Test that _get_assembly_utterances returns the utterances from a valid AssemblyAI json file."""
    assembly_json: Dict[str, List[Dict[str, Union[int, str]]]] = {
        "utterances": [
            {"speaker": 0, "elements": "Hello world."},
            {"speaker": 0, "elements": "How are you?"},
            {"speaker": 1, "elements": "I am fine."},
        ],
    }
    expected_output = assembly_json["utterances"]
    assert _get_assembly_utterances(assembly_json) == expected_output


def test_get_assembly_utterances_missing_utterances() -> None:
    """Test that _get_assembly_utterances raises a ValueError when the input json is missing the 'utterances' key."""
    assembly_json: Dict[str, str] = {}
    with pytest.raises(
        ValueError,
        match="No utterances key found. Verify the AssemblyAI json file you are using.",
    ):
        _get_assembly_utterances(assembly_json)


def test_get_deepgram_utterances_valid() -> None:
    """Test that _get_deepgram_utterances returns the utterances from a valid Deepgram json file."""
    deepgram_json: Dict[str, Dict[str, List[Dict[str, Union[int, str]]]]] = {
        "results": {
            "utterances": [
                {"speaker": 0, "transcript": "Hello world."},
                {"speaker": 0, "transcript": "How are you?"},
            ]
        }
    }
    expected_output = deepgram_json["results"]["utterances"]
    assert _get_deepgram_utterances(deepgram_json) == expected_output


def test_get_deepgram_utterances_missing_results() -> None:
    """Test that _get_deepgram_utterances raises a ValueError when the input json is missing the 'results' key."""
    deepgram_json: Dict[str, str] = {}
    with pytest.raises(
        ValueError,
        match="No results key found. Verify the Deepgram json file you are using.",
    ):
        _get_deepgram_utterances(deepgram_json)


def test_get_deepgram_utterances_missing_utterances() -> None:
    """Test that _get_deepgram_utterances raises a ValueError when the input json is missing the 'utterances' key."""
    deepgram_json: Dict[str, Dict[str, str]] = {"results": {}}
    with pytest.raises(
        ValueError,
        match="No utterances key found. Verify the Deepgram json file you are using.",
    ):
        _get_deepgram_utterances(deepgram_json)


def test_get_rev_monologues_valid() -> None:
    """Test that _get_rev_monologues returns the monologues from a valid Rev json file."""
    rev_json: Dict[str, List[Dict[str, Union[int, str]]]] = {
        "monologues": [
            {"speaker": 0, "elements": "Hello world."},
            {"speaker": 1, "elements": "How are you?"},
            {"speaker": 0, "elements": "I am fine."},
        ]
    }
    expected_output = rev_json["monologues"]
    assert _get_rev_monologues(rev_json) == expected_output


def test_get_rev_monologues_missing_monologues() -> None:
    """Test that _get_rev_monologues raises a ValueError when the input json is missing the 'monologues' key."""
    rev_json: Dict[str, str] = {}
    with pytest.raises(
        ValueError,
        match="No monologues key found. Verify the Rev.ai json file you are using.",
    ):
        _get_rev_monologues(rev_json)
