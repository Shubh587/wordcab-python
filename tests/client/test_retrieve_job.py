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

"""Test suite for the Client retrieve_job method."""

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import ExtractJob, SummarizeJob


class TestClientRetrieveJob:
    """Test suite for the Client retrieve_job method."""

    extract_job = {
        "job_name": "job_98765",
        "job_status": "ExtractionComplete",
        "time_started": "2022-10-21T13:28:14.137458Z",
        "transcript_id": "generic_transcript_98765",
        "display_name": "Data Extraction Example",
        "settings": {
            "pipeline": "questions_answers,topic_segments,emotions,speaker_talk_ratios",
            "split_long_utterances": False,
            "ephemeral_data": False,
            "only_api": False,
        },
        "source": "generic",
        "source_lang": None,
        "target_lang": None,
        "transcript_details": {
            "asr_engine": "asr_wordcab",
            "alignment": True,
            "diarization": True,
            "dual_channel": False,
            "word_timestamps": True,
            "show_disfluencies": False,
            "show_numerals": False,
            "vocab": [],
            "num_speakers": None,
        },
        "metadata": {},
        "tags": [],
        "time_completed": "2022-10-21T13:38:06.723662+00:00",
    }
    summarize_job = {
        "job_name": "job_12345",
        "job_status": "SummaryComplete",
        "time_started": "2023-01-21T10:03:14.906439Z",
        "transcript_id": "audio_transcript_12345",
        "display_name": "I Love Summarization",
        "settings": {
            "pipeline": "transcribe,summarize",
            "split_long_utterances": False,
            "ephemeral_data": False,
            "only_api": True,
        },
        "source": "audio",
        "source_lang": "en",
        "target_lang": "en",
        "transcript_details": {
            "asr_engine": "asr_wordcab",
            "alignment": True,
            "diarization": True,
            "dual_channel": False,
            "word_timestamps": True,
            "show_disfluencies": False,
            "show_numerals": False,
            "vocab": [],
            "num_speakers": None,
        },
        "summary_details": {
            "summary_id": "narrative_summary_12345",
            "summary_type": "narrative",
            "summary_lens": [1, 3, 5],
        },
        "metadata": {},
        "tags": ["customer_name", "agent_name"],
        "time_completed": "2023-01-21T10:05:08.021499+00:00",
    }

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_retrieve_summarize_job(self, api_key, mock_server) -> None:
        """Test client retrieve_job method for summarize job."""
        with Client(api_key=api_key) as client:
            job_name = self.summarize_job["job_name"]
            mock_server.add(
                responses.GET,
                url=f"https://wordcab.com/api/v1/jobs/{job_name}",
                json=self.summarize_job,
                status=200,
            )
            job = client.retrieve_job(job_name=self.summarize_job["job_name"])
            assert job.job_name == self.summarize_job["job_name"]
            assert job is not None
            assert isinstance(job, SummarizeJob)
            assert job.job_status is not None
            assert job.display_name is not None
            assert job.source is not None
            assert job.source_lang is not None
            assert job.target_lang is not None
            assert job.time_started is not None
            assert job.time_completed is not None
            assert job.transcript_details is not None
            assert job.transcript_id is not None
            assert job.summary_details is not None
            assert isinstance(job.summary_details, dict)

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_retrieve_extract_job(self, api_key, mock_server) -> None:
        """Test client retrieve_job method for extract job."""
        with Client(api_key=api_key) as client:
            job_name = self.extract_job["job_name"]
            mock_server.add(
                responses.GET,
                url=f"https://wordcab.com/api/v1/jobs/{job_name}",
                json=self.extract_job,
                status=200,
            )
            job = client.retrieve_job(job_name=self.extract_job["job_name"])
            assert job.job_name == self.extract_job["job_name"]
            assert job is not None
            assert isinstance(job, ExtractJob)
            assert job.job_status is not None
            assert job.display_name is not None
            assert job.source is not None
            assert job.source_lang is None
            assert job.target_lang is None
            assert job.time_started is not None
            assert job.time_completed is not None
            assert job.transcript_details is not None
            assert job.transcript_id is not None
