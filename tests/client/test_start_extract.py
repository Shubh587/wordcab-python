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

"""Test suite for the Client start_extract method."""

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import ExtractJob, JobSettings


class TestClientStartExtract:
    """Test suite for the Client start_extract method."""

    @pytest.mark.usefixtures("api_key", "generic_source_txt")
    def test_start_extract_invalid(
        self,
        base_source,
        api_key,
        generic_source_txt,
    ) -> None:
        """Test client start_extract method."""
        with Client(api_key=api_key) as client:
            with pytest.raises(ValueError):
                client.start_extract(
                    source_object=base_source, display_name="test-extraction"
                )
            with pytest.raises(ValueError):
                client.start_extract(
                    source_object=generic_source_txt,
                    display_name="test-extraction",
                    pipelines=["invalid"],
                )
            with pytest.raises(ValueError):
                client.start_extract(
                    source_object={"invalid": "invalid"}, display_name="test-extraction"
                )
            with pytest.raises(ValueError):
                base_source.source = "generic"
                client.start_extract(
                    source_object=base_source, display_name="test-extraction"
                )

    @pytest.mark.usefixtures("api_key", "generic_source_txt", "mock_server")
    def test_start_extract_txt_file(
        self,
        api_key,
        generic_source_txt,
        mock_server,
    ) -> None:
        """Test client start_extract method with txt file."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/extract",
                json={"job_name": "job_12345"},
                status=201,
            )
            txt_job = client.start_extract(
                source_object=generic_source_txt,
                display_name="test-extraction-txt",
                pipelines=["emotions"],
            )

        assert isinstance(txt_job, ExtractJob)
        assert txt_job.display_name == "test-extraction-txt"
        assert txt_job.job_name is not None
        assert txt_job.source == "generic"
        assert txt_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="emotions",
            split_long_utterances=False,
            only_api=True,
        )

    @pytest.mark.usefixtures("api_key", "generic_source_json", "mock_server")
    def test_start_extract_json_file(
        self,
        api_key,
        generic_source_json,
        mock_server,
    ) -> None:
        """Test client start_extract method with json file."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/extract",
                json={"job_name": "job_12345"},
                status=201,
            )
            json_job = client.start_extract(
                source_object=generic_source_json,
                display_name="test-extraction-json",
                pipelines=["emotions"],
            )

        assert isinstance(json_job, ExtractJob)

        assert json_job.job_name is not None
        assert json_job.job_name == "job_12345"

        assert json_job.display_name == "test-extraction-json"
        assert json_job.source == "generic"

        assert json_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="emotions",
            split_long_utterances=False,
            only_api=True,
        )

    @pytest.mark.usefixtures("api_key", "audio_source", "mock_server")
    def test_start_extract_audio_file(
        self,
        api_key,
        audio_source,
        mock_server,
    ) -> None:
        """Test client start_extract method with audio file."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.POST,
                url="https://wordcab.com/api/v1/extract",
                json={"job_name": "job_12345"},
                status=201,
            )
            audio_job = client.start_extract(
                source_object=audio_source,
                display_name="test-extraction-audio",
                pipelines=["emotions"],
            )

        assert isinstance(audio_job, ExtractJob)

        assert audio_job.job_name is not None
        assert audio_job.job_name == "job_12345"

        assert audio_job.display_name == "test-extraction-audio"
        assert audio_job.source == "audio"

        assert audio_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="emotions",
            split_long_utterances=False,
            only_api=True,
        )
