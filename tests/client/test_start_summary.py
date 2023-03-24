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

"""Test suite for the Client start_summary method."""

from typing import List

import pytest

from wordcab.client import Client
from wordcab.core_objects import (
    AudioSource,
    BaseSource,
    DeepgramSource,
    GenericSource,
    InMemorySource,
    JobSettings,
    SummarizeJob,
    WordcabTranscriptSource,
)


def test_start_summary_errors(
    base_source: BaseSource,
    generic_source_txt: GenericSource,
    api_key: str,
) -> None:
    """Test client start_summary method."""
    with Client(api_key=api_key) as client:
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source_txt,
                display_name="test",
                summary_type="invalid",
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source_txt,
                display_name="test",
                summary_type="narrative",
                summary_lens=0,
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source_txt,
                display_name="test",
                summary_type="narrative",
                summary_lens=3,
                pipelines=["invalid"],
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object={"invalid": "invalid"},  # type: ignore
                display_name="test",
                summary_type="narrative",
                summary_lens=3,
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=base_source,
                display_name="test",
                summary_type="narrative",
                summary_lens=3,
            )
        with pytest.raises(ValueError):
            base_source.source = "generic"
            client.start_summary(
                source_object=base_source,
                display_name="test",
                summary_type="narrative",
                summary_lens=3,
            )


def test_summary_in_memory(in_memory_source: InMemorySource, api_key: str) -> None:
    """Test client start_summary method with in-memory source."""
    with Client(api_key=api_key) as client:
        in_memory_job = client.start_summary(
            source_object=in_memory_source,
            display_name="test-sdk-in-memory",
            summary_type="conversational",
            summary_lens=3,
        )
        assert isinstance(in_memory_job, SummarizeJob)
        assert in_memory_job.display_name == "test-sdk-in-memory"
        assert in_memory_job.job_name is not None
        assert in_memory_job.source == "generic"
        assert in_memory_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_summary_generic_txt(generic_source_txt: GenericSource, api_key: str) -> None:
    """Test client start_summary method with generic text source."""
    with Client(api_key=api_key) as client:
        txt_job = client.start_summary(
            source_object=generic_source_txt,
            display_name="test-sdk-txt",
            summary_type="no_speaker",
        )
        assert isinstance(txt_job, SummarizeJob)
        assert txt_job.display_name == "test-sdk-txt"
        assert txt_job.job_name is not None
        assert txt_job.source == "generic"
        assert txt_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_start_summary_generic_context(
    context_elements: List[str], generic_source_txt: GenericSource, api_key: str
) -> None:
    """Test client start_summary method with generic text source."""
    with Client(api_key=api_key) as client:
        txt_job = client.start_summary(
            source_object=generic_source_txt,
            display_name="test-sdk-txt",
            summary_type="narrative",
            context=context_elements,
        )
        assert isinstance(txt_job, SummarizeJob)
        assert txt_job.display_name == "test-sdk-txt"
        assert txt_job.job_name is not None
        assert txt_job.source == "generic"
        assert txt_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_start_summary_generic_json(
    generic_source_json: GenericSource, api_key: str
) -> None:
    """Test client start_summary method with generic json source."""
    with Client(api_key=api_key) as client:
        json_job = client.start_summary(
            source_object=generic_source_json,
            display_name="test-sdk-json",
            summary_type="narrative",
            summary_lens=3,
        )
        assert isinstance(json_job, SummarizeJob)
        assert json_job.display_name == "test-sdk-json"
        assert json_job.job_name is not None
        assert json_job.source == "generic"
        assert json_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_start_summary_generic_url(
    generic_url_json: GenericSource, api_key: str
) -> None:
    """Test client start_summary method with generic url source."""
    with Client(api_key=api_key) as client:
        json_job = client.start_summary(
            source_object=generic_url_json,
            display_name="test-sdk-json-url",
            summary_type="brief",
            summary_lens=3,
        )
        assert isinstance(json_job, SummarizeJob)
        assert json_job.display_name == "test-sdk-json-url"
        assert json_job.job_name is not None
        assert json_job.source == "generic"
        assert json_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_start_summary_audio(audio_source: AudioSource, api_key: str) -> None:
    """Test client start_summary method with audio source."""
    with Client(api_key=api_key) as client:
        audio_job = client.start_summary(
            source_object=audio_source,
            display_name="test-sdk-audio",
            summary_type="narrative",
            summary_lens=3,
        )
        assert isinstance(audio_job, SummarizeJob)
        assert audio_job.display_name == "test-sdk-audio"
        assert audio_job.job_name is not None
        assert audio_job.source == "audio"
        assert audio_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_start_summary_audio_url(audio_url_source: AudioSource, api_key: str) -> None:
    """Test client start_summary method with audio url source."""
    with Client(api_key=api_key) as client:
        audio_job = client.start_summary(
            source_object=audio_url_source,
            display_name="test-sdk-audio-url",
            summary_type="narrative",
            summary_lens=3,
        )
        assert isinstance(audio_job, SummarizeJob)
        assert audio_job.display_name == "test-sdk-audio-url"
        assert audio_job.job_name is not None
        assert audio_job.source == "audio"
        assert audio_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_start_summary_wordcab_transcript(api_key: str) -> None:
    """Test client start_summary method with WordcabTranscriptSource."""
    with Client(api_key=api_key) as client:
        wordcab_transcript_job = client.start_summary(
            source_object=WordcabTranscriptSource(
                transcript_id="generic_transcript_MXzewRcYCnJXKFTLewMYC53uTNyWCEeo"
            ),
            display_name="test-sdk-wordcab-transcript",
            summary_type="narrative",
            summary_lens=1,
        )
        assert isinstance(wordcab_transcript_job, SummarizeJob)
        assert wordcab_transcript_job.display_name == "test-sdk-wordcab-transcript"
        assert wordcab_transcript_job.job_name is not None
        assert wordcab_transcript_job.source == "wordcab_transcript"
        assert wordcab_transcript_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_start_summary_deepgram_transcript(api_key: str) -> None:
    """Test client start_summary method with DeepgramSource."""
    with Client(api_key=api_key) as client:
        dg_transcript_job = client.start_summary(
            source_object=DeepgramSource(
                filepath="tests/deepgram_sample.json",
            ),
            display_name="test-sdk-dg-transcript",
            summary_type="narrative",
            summary_lens=1,
        )
        assert isinstance(dg_transcript_job, SummarizeJob)
        assert dg_transcript_job.display_name == "test-sdk-dg-transcript"
        assert dg_transcript_job.job_name is not None
        assert dg_transcript_job.source == "deepgram"
        assert dg_transcript_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )
