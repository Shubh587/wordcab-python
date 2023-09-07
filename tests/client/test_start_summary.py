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

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import (
    AssemblyAISource,
    DeepgramSource,
    JobSettings,
    RevSource,
    SummarizeJob,
    VTTSource,
    WordcabTranscriptSource,
)


class TestClientStartSummary:
    """Test suite for the Client start_summary method."""

    @pytest.mark.usefixtures("api_key", "generic_source_txt")
    def test_start_summary_errors(
        self,
        base_source,
        generic_source_txt,
        api_key,
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

    @pytest.mark.usefixtures("api_key", "in_memory_source", "mock_server")
    def test_summary_in_memory(self, in_memory_source, api_key, mock_server) -> None:
        """Test client start_summary method with in-memory source."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            in_memory_job = client.start_summary(
                source_object=in_memory_source,
                display_name="test-sdk-in-memory",
                summary_type="conversational",
                summary_lens=3,
            )
            assert isinstance(in_memory_job, SummarizeJob)
            assert in_memory_job.display_name == "test-sdk-in-memory"
            assert in_memory_job.job_name is not None
            assert in_memory_job.job_name == "job_12345"
            assert in_memory_job.source == "generic"
            assert in_memory_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "generic_source_txt", "mock_server")
    def test_summary_generic_txt(
        self, generic_source_txt, api_key, mock_server
    ) -> None:
        """Test client start_summary method with generic text source."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            txt_job = client.start_summary(
                source_object=generic_source_txt,
                display_name="test-sdk-txt",
                summary_type="no_speaker",
            )
            assert isinstance(txt_job, SummarizeJob)
            assert txt_job.display_name == "test-sdk-txt"
            assert txt_job.job_name is not None
            assert txt_job.job_name == "job_12345"
            assert txt_job.source == "generic"
            assert txt_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures(
        "api_key", "context_elements", "generic_source_json", "mock_server"
    )
    def test_start_summary_generic_context(
        self,
        context_elements,
        generic_source_txt,
        api_key,
        mock_server,
    ) -> None:
        """Test client start_summary method with generic text source."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            txt_job = client.start_summary(
                source_object=generic_source_txt,
                display_name="test-sdk-txt",
                summary_type="narrative",
                context=context_elements,
            )
            assert isinstance(txt_job, SummarizeJob)
            assert txt_job.display_name == "test-sdk-txt"
            assert txt_job.job_name is not None
            assert txt_job.job_name == "job_12345"
            assert txt_job.source == "generic"
            assert txt_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "generic_source_json", "mock_server")
    def test_start_summary_generic_json(
        self,
        generic_source_json,
        api_key,
        mock_server,
    ) -> None:
        """Test client start_summary method with generic json source."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            json_job = client.start_summary(
                source_object=generic_source_json,
                display_name="test-sdk-json",
                summary_type="narrative",
                summary_lens=3,
            )
            assert isinstance(json_job, SummarizeJob)
            assert json_job.display_name == "test-sdk-json"
            assert json_job.job_name is not None
            assert json_job.job_name == "job_12345"
            assert json_job.source == "generic"
            assert json_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "generic_url_json", "mock_server")
    def test_start_summary_generic_url(
        self,
        generic_url_json,
        api_key,
        mock_server,
    ) -> None:
        """Test client start_summary method with generic url source."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            json_job = client.start_summary(
                source_object=generic_url_json,
                display_name="test-sdk-json-url",
                summary_type="brief",
                summary_lens=3,
            )
            assert isinstance(json_job, SummarizeJob)
            assert json_job.display_name == "test-sdk-json-url"
            assert json_job.job_name is not None
            assert json_job.job_name == "job_12345"
            assert json_job.source == "generic"
            assert json_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("audio_source", "api_key", "mock_server")
    def test_start_summary_audio(self, audio_source, api_key, mock_server) -> None:
        """Test client start_summary method with audio source."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            audio_job = client.start_summary(
                source_object=audio_source,
                display_name="test-sdk-audio",
                summary_type="narrative",
                summary_lens=3,
            )
            assert isinstance(audio_job, SummarizeJob)
            assert audio_job.display_name == "test-sdk-audio"
            assert audio_job.job_name is not None
            assert audio_job.job_name == "job_12345"
            assert audio_job.source == "audio"
            assert audio_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("audio_url_source", "api_key", "mock_server")
    def test_start_summary_audio_url(
        self, audio_url_source, api_key, mock_server
    ) -> None:
        """Test client start_summary method with audio url source."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            audio_job = client.start_summary(
                source_object=audio_url_source,
                display_name="test-sdk-audio-url",
                summary_type="narrative",
                summary_lens=3,
            )
            assert isinstance(audio_job, SummarizeJob)
            assert audio_job.display_name == "test-sdk-audio-url"
            assert audio_job.job_name is not None
            assert audio_job.job_name == "job_12345"
            assert audio_job.source == "audio"
            assert audio_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_start_summary_wordcab_transcript(self, api_key, mock_server) -> None:
        """Test client start_summary method with WordcabTranscriptSource."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            wordcab_transcript_job = client.start_summary(
                source_object=WordcabTranscriptSource(
                    transcript_id="generic_transcript_12345"
                ),
                display_name="test-sdk-wordcab-transcript",
                summary_type="narrative",
                summary_lens=1,
            )
            assert isinstance(wordcab_transcript_job, SummarizeJob)
            assert wordcab_transcript_job.display_name == "test-sdk-wordcab-transcript"
            assert wordcab_transcript_job.job_name is not None
            assert wordcab_transcript_job.job_name == "job_12345"
            assert wordcab_transcript_job.source == "wordcab_transcript"
            assert wordcab_transcript_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_start_summary_deepgram_transcript(self, api_key, mock_server) -> None:
        """Test client start_summary method with DeepgramSource."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
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
            assert dg_transcript_job.job_name == "job_12345"
            assert dg_transcript_job.source == "deepgram"
            assert dg_transcript_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_start_summary_rev_transcript(self, api_key, mock_server) -> None:
        """Test client start_summary method with RevSource."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            rev_transcript_job = client.start_summary(
                source_object=RevSource(
                    filepath="tests/rev_sample.json",
                ),
                display_name="test-sdk-rev-transcript",
                summary_type="narrative",
                summary_lens=1,
            )
            assert isinstance(rev_transcript_job, SummarizeJob)
            assert rev_transcript_job.display_name == "test-sdk-rev-transcript"
            assert rev_transcript_job.job_name is not None
            assert rev_transcript_job.job_name == "job_12345"
            assert rev_transcript_job.source == "rev_ai"
            assert rev_transcript_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_start_summary_assembly_transcript(self, api_key, mock_server) -> None:
        """Test client start_summary method with AssemblyAISource."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/summarize",
                json={"job_name": "job_12345"},
                status=201,
            )
            assembly_transcript_job = client.start_summary(
                source_object=AssemblyAISource(
                    filepath="tests/assembly_sample.json",
                ),
                display_name="test-sdk-assembly-transcript",
                summary_type="narrative",
                summary_lens=1,
            )
            assert isinstance(assembly_transcript_job, SummarizeJob)
            assert (
                assembly_transcript_job.display_name == "test-sdk-assembly-transcript"
            )
            assert assembly_transcript_job.job_name is not None
            assert assembly_transcript_job.job_name == "job_12345"
            assert assembly_transcript_job.source == "assembly_ai"
            assert assembly_transcript_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe,summarize",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key")
    def test_start_summary_vtt_transcript(self, api_key) -> None:
        """Test client start_summary method with VTTSource."""
        with pytest.raises(ValueError):  # monkeypatch, api needs a vtt fix
            with Client(api_key=api_key) as client:
                vtt_transcript_job = client.start_summary(
                    source_object=VTTSource(
                        filepath="tests/vtt_sample.vtt",
                    ),
                    display_name="test-sdk-vtt-transcript",
                    summary_type="narrative",
                    summary_lens=1,
                )

                assert isinstance(vtt_transcript_job, SummarizeJob)
                assert vtt_transcript_job.display_name == "test-sdk-vtt-transcript"
                assert vtt_transcript_job.job_name is not None
                assert vtt_transcript_job.source == "vtt"
                assert vtt_transcript_job.settings == JobSettings(
                    ephemeral_data=False,
                    pipeline="transcribe,summarize",
                    split_long_utterances=False,
                    only_api=True,
                )
