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
from typing import Any, Dict

from wordcab.core_objects.utils import _get_context_items, _textwrap


def test_textwrap_default_width() -> None:
    """Test that _textwrap wraps the text to the default width of 80."""
    text_to_wrap = "This is a long text that should be wrapped to the specified width of 80 characters by default."

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
        "Issue: This is an issue\n"
        "Purpose: This is a purpose\n"
        "Next steps: {'text': 'These are next steps', 'associated_speakers': ['SPEAKER B']}\n"
        "Discussion points: ['These are discussion points', 'These are more discussion points']\n"
        "Keywords: ['These are keywords', 'These are more keywords']\n"
    )
    assert expected_result == result


def test_no_context_items() -> None:
    """Test that _get_context_items returns an empty string when there are no context items."""
    context: Dict[str, Any] = {}

    result = _get_context_items(context)

    assert "" == result
