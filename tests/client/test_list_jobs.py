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

"""Test suite for the Client list_jobs method."""

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import ListJobs


class TestClientListJobs:
    """Test suite for the Client list_jobs method."""

    jobs = {
        "page_count": 2,
        "next": "https://wordcab.com/api/v1/jobs?page=2",
        "results": [
            {
                "job_status": "Pending",
                "job_name": "job_123",
                "display_name": "file_transcript_2023_09_04",
                "transcript_id": "file_transcript_123",
                "source": "audio",
                "time_started": "2023-09-04T11:50:08.700803Z",
                "time_completed": "2023-09-04T11:50:15.366268+00:00",
            },
            {
                "job_status": "TranscriptComplete",
                "job_name": "job_456",
                "display_name": "file_transcript_2023_09_03",
                "transcript_id": "file_transcript_456",
                "source": "audio",
                "time_started": "2023-09-04T11:49:02.073268Z",
                "time_completed": "2023-09-04T11:49:13.825813+00:00",
            },
            {
                "job_status": "TranscriptComplete",
                "job_name": "job_789",
                "display_name": "file_transcript_2023_09_02",
                "transcript_id": "file_transcript_789",
                "source": "audio",
                "time_started": "2023-09-04T11:49:02.003423Z",
                "time_completed": "2023-09-04T11:49:12.507622+00:00",
            },
        ],
    }

    @pytest.mark.usefixtures("api_key", "mock_server")
    def test_list_jobs(self, api_key, mock_server) -> None:
        """Test client list_jobs method."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.GET,
                "https://wordcab.com/api/v1/jobs",
                json=self.jobs,
                status=200,
            )
            list_jobs = client.list_jobs()

            assert list_jobs is not None
            assert isinstance(list_jobs, ListJobs)

            assert list_jobs.page_count is not None
            assert isinstance(list_jobs.page_count, int)

            assert list_jobs.next_page is not None
            assert list_jobs.next_page == "https://wordcab.com/api/v1/jobs?page=2"
            assert isinstance(list_jobs.next_page, str)

            assert list_jobs.results is not None
            assert len(list_jobs.results) == 3
            assert isinstance(list_jobs.results, list)

            assert list_jobs.results[0].job_status == "Pending"
            assert list_jobs.results[0].job_name == "job_123"
            assert list_jobs.results[0].display_name == "file_transcript_2023_09_04"
            assert list_jobs.results[0].transcript_id == "file_transcript_123"
            assert list_jobs.results[0].source == "audio"
            assert list_jobs.results[0].time_started == "2023-09-04T11:50:08.700803Z"
            assert (
                list_jobs.results[0].time_completed
                == "2023-09-04T11:50:15.366268+00:00"
            )

            assert list_jobs.results[1].job_status == "TranscriptComplete"
            assert list_jobs.results[1].job_name == "job_456"
            assert list_jobs.results[1].display_name == "file_transcript_2023_09_03"
            assert list_jobs.results[1].transcript_id == "file_transcript_456"
            assert list_jobs.results[1].source == "audio"
            assert list_jobs.results[1].time_started == "2023-09-04T11:49:02.073268Z"
            assert (
                list_jobs.results[1].time_completed
                == "2023-09-04T11:49:13.825813+00:00"
            )

            assert list_jobs.results[2].job_status == "TranscriptComplete"
            assert list_jobs.results[2].job_name == "job_789"
            assert list_jobs.results[2].display_name == "file_transcript_2023_09_02"
            assert list_jobs.results[2].transcript_id == "file_transcript_789"
            assert list_jobs.results[2].source == "audio"
            assert list_jobs.results[2].time_started == "2023-09-04T11:49:02.003423Z"
            assert (
                list_jobs.results[2].time_completed
                == "2023-09-04T11:49:12.507622+00:00"
            )

    @pytest.mark.usefixtures("api_key")
    def test_error_list_jobs(self, api_key) -> None:
        """Test client list_jobs method with error."""
        with Client(api_key=api_key) as client:
            with pytest.raises(ValueError):
                client.list_jobs(order_by="invalid")
            with pytest.raises(ValueError):
                client.list_jobs(order_by="+time_started")
            with pytest.raises(ValueError):
                client.list_jobs(order_by="+time_completed")
