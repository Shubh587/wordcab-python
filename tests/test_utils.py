# Copyright 2022 The Wordcab Team. All rights reserved.
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

"""Test cases for the utils functions."""

from typing import List, Union

import pytest

from wordcab.utils import (
    _check_context_elements,
    _check_source_lang,
    _check_summary_length,
    _check_summary_pipelines,
    _format_context_elements,
    _format_lengths,
    _format_pipelines,
    _format_tags,
)


@pytest.mark.parametrize(
    "elements", ["test_element", ["element1", "element2"], ["test"]]
)
def test_format_context_elements(elements: Union[str, List[str]]) -> None:
    """Test format context elements."""
    if isinstance(elements, str):
        assert _format_context_elements(elements=elements) == elements
    else:
        assert _format_context_elements(elements=elements) == ",".join(elements)


@pytest.mark.parametrize(
    "elements",
    ["next_steps", ["keywords"], ["discussion_points", "next_steps", "issue"]],
)
def test_correct_check_context_elements(elements: Union[str, List[str]]) -> None:
    """Test correct context elements."""
    assert _check_context_elements(elements=elements) is True


@pytest.mark.parametrize(
    "elements", ["test_element", ["element1", "element2"], ["kwords"], [1, 2]]
)
def test_wrong_check_context_elements(elements: Union[str, List[str]]) -> None:
    """Test wrong context elements."""
    assert _check_context_elements(elements=elements) is False


@pytest.mark.parametrize("lang", ["en", "es", "de", "fr", "it"])
def test_correct_check_source_lang(lang: str) -> None:
    """Test correct source languages."""
    assert _check_source_lang(lang=lang) is True


@pytest.mark.parametrize("lang", ["en-US", "es-ES", "de-DE", "fr-FR", "ru", "ja", "zh"])
def test_wrong_check_source_lang(lang: str) -> None:
    """Test wrong source languages."""
    assert _check_source_lang(lang=lang) is False


@pytest.mark.parametrize("lengths", [50, [50, 100]])
def test_wrong_check_summary_length(lengths: Union[int, List[int]]) -> None:
    """Test wrong summary lengths."""
    assert _check_summary_length(lengths=lengths) is False


@pytest.mark.parametrize("lengths", [1, 2, 3, 4, 5, [3, 5]])
def test_correct_check_summary_length(lengths: Union[int, List[int]]) -> None:
    """Test correct summary lengths."""
    assert _check_summary_length(lengths=lengths) is True


@pytest.mark.parametrize(
    "pipelines",
    [
        "emotions",
        "questions_answers",
        "topic_segments",
        "speaker_talk_ratios",
        ["pipeline1", "pipeline2"],
    ],
)
def test_wrong_check_summary_pipelines(pipelines: Union[str, List[str]]) -> None:
    """Test wrong summary pipelines."""
    assert _check_summary_pipelines(pipelines=pipelines) is False


@pytest.mark.parametrize(
    "pipelines", ["transcribe", "summarize", ["transcribe", "summarize"]]
)
def test_correct_check_summary_pipelines(pipelines: Union[str, List[str]]) -> None:
    """Test correct summary pipelines."""
    assert _check_summary_pipelines(pipelines=pipelines) is True


@pytest.mark.parametrize("lengths", [1, [1, 2, 5]])
def test_format_lengths(lengths: Union[int, List[int]]) -> None:
    """Test format lengths."""
    if isinstance(lengths, int):
        assert _format_lengths(lengths=lengths) == str(lengths)
    else:
        assert _format_lengths(lengths=lengths) == ",".join(
            [str(length) for length in lengths]
        )


@pytest.mark.parametrize(
    "pipelines", ["transcribe", "summarize", ["transcribe", "summarize"]]
)
def test_format_pipelines(pipelines: Union[str, List[str]]) -> None:
    """Test format pipelines."""
    if isinstance(pipelines, str):
        assert _format_pipelines(pipelines=pipelines) == pipelines
    else:
        assert _format_pipelines(pipelines=pipelines) == ",".join(pipelines)


@pytest.mark.parametrize(
    "tags", ["test_tag", ["tag1", "tag2"], ["tag1", "tag2", "tag3"]]
)
def test_format_tags(tags: Union[str, List[str]]) -> None:
    """Test format tags."""
    if isinstance(tags, str):
        assert _format_tags(tags=tags) == tags
    else:
        assert _format_tags(tags=tags) == ",".join(tags)
