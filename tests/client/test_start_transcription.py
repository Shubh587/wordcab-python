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

"""Test suite for the Client start_transcription method."""

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import (
    JobSettings,
    TranscribeJob,
)


class TestClientStartTranscription:
    """Test suite for the Client start_transcription method."""

    @pytest.mark.usefixtures("api_key", "audio_url_source_no_download")
    def test_start_transcription_errors(
        self,
        audio_url_source_no_download,
        api_key,
    ) -> None:
        with Client(api_key=api_key) as client:
            with pytest.raises(ValueError):
                client.start_transcription(
                    source_object=audio_url_source_no_download,
                    display_name="test_display_name",
                    source_lang="en-US",
                    api_key=api_key,
                )

    @pytest.mark.usefixtures("api_key", "audio_url_source_no_download", "mock_server")
    def test_start_transcription_audio_no_download(
        self,
        audio_url_source_no_download,
        api_key,
        mock_server,
    ) -> None:
        """Test the start_transcription method."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/transcribe",
                json={"job_name": "test_job_name"},
                status=200,
            )
            transcribe_job = client.start_transcription(
                source_object=audio_url_source_no_download,
                display_name="test_display_name",
                source_lang="en",
                api_key=api_key,
            )
            assert isinstance(transcribe_job, TranscribeJob)
            assert transcribe_job.job_name == "test_job_name"
            assert transcribe_job.source == "audio"
            assert transcribe_job.display_name == "test_display_name"
            assert transcribe_job.source_lang == "en"
            assert transcribe_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "audio_url_source_with_download", "mock_server")
    def test_start_transcription_audio_with_download(
        self,
        audio_url_source_with_download,
        api_key,
        mock_server,
    ) -> None:
        """Test the start_transcription method with downloaded audio."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/transcribe",
                json={"job_name": "test_job_name"},
                status=200,
            )
            transcribe_job = client.start_transcription(
                source_object=audio_url_source_with_download,
                display_name="test_display_name",
                source_lang="en",
                api_key=api_key,
            )
            assert isinstance(transcribe_job, TranscribeJob)
            assert transcribe_job.job_name == "test_job_name"
            assert transcribe_job.source == "audio"
            assert transcribe_job.display_name == "test_display_name"
            assert transcribe_job.source_lang == "en"
            assert transcribe_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe",
                split_long_utterances=False,
                only_api=True,
            )

    @pytest.mark.usefixtures("api_key", "youtube_source", "mock_server")
    def test_start_transcription_youtube(
        self,
        youtube_source,
        api_key,
        mock_server,
    ) -> None:
        """Test the start_transcription method with a YouTube video."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/transcribe",
                json={"job_name": "test_job_name"},
                status=200,
            )
            transcribe_job = client.start_transcription(
                source_object=youtube_source,
                display_name="test_display_name",
                source_lang="en",
                api_key=api_key,
            )
            assert isinstance(transcribe_job, TranscribeJob)
            assert transcribe_job.job_name == "test_job_name"
            assert transcribe_job.source == "youtube"
            assert transcribe_job.display_name == "test_display_name"
            assert transcribe_job.source_lang == "en"
            assert transcribe_job.settings == JobSettings(
                ephemeral_data=False,
                pipeline="transcribe",
                split_long_utterances=False,
                only_api=True,
            )
