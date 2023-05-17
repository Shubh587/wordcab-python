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

from wordcab.client import Client
from wordcab.core_objects import ExtractJob, SummarizeJob


def test_retrieve_summarize_job(api_key: str) -> None:
    """Test client retrieve_job method for summarize job."""
    with Client(api_key=api_key) as client:
        job = client.retrieve_job(job_name="job_QeYrPCc5mc43TaHsyXEk4eF6Bejg2gDU")
        assert job.job_name == "job_QeYrPCc5mc43TaHsyXEk4eF6Bejg2gDU"
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


def test_retrieve_extract_job(api_key: str) -> None:
    """Test client retrieve_job method for extract job."""
    with Client(api_key=api_key) as client:
        job = client.retrieve_job(job_name="job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n")
        assert job.job_name == "job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n"
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
