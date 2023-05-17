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

"""Test suite for the API retrieve_job function."""

from wordcab.api import retrieve_job
from wordcab.core_objects import ExtractJob, SummarizeJob


def test_api_retrieve_job(api_key: str) -> None:
    """Test the retrieve_job function."""
    job = retrieve_job(job_name="job_VkzpZbp79KVv4SoTiW8bFATY4FVQ9rCp", api_key=api_key)
    assert job.job_name == "job_VkzpZbp79KVv4SoTiW8bFATY4FVQ9rCp"
    assert job is not None
    assert isinstance(job, SummarizeJob)
    assert job.job_status is not None
    assert job.display_name is not None
    assert job.source is not None
    assert job.time_started is not None
    assert job.time_completed is not None
    assert job.transcript_details is not None
    assert job.transcript_id is not None
    assert job.summary_details is not None
    assert isinstance(job.summary_details, dict)

    # Extract job
    job = retrieve_job(job_name="job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n", api_key=api_key)
    assert job.job_name == "job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n"
    assert job is not None
    assert isinstance(job, ExtractJob)
    assert job.job_status is not None
    assert job.display_name is not None
    assert job.source is not None
    assert job.time_started is not None
    assert job.time_completed is not None
    assert job.transcript_details is not None
    assert job.transcript_id is not None
