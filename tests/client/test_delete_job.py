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

"""Test suite for the Client delete_job method."""

import pytest
import responses
from wordcab.client import Client


class TestClientDeleteJob:
    """Test suite for the Client delete_job method."""

    @pytest.mark.usefixtures("api_key", "get_job_name", "mock_server")
    def test_delete_job(api_key, get_job_name, mock_server) -> None:
        """Test client delete_job method."""
        with Client(api_key=api_key) as client:
            mock_server.add(
                responses.DELETE,
                f"https://wordcab.com/api/v1/jobs/{get_job_name}",
                json={"job_name": get_job_name},
                status=200,
            )
            deleted_job = client.delete_job(job_name=get_job_name)

            assert deleted_job is not None
            assert isinstance(deleted_job, dict)
            assert deleted_job["job_name"] == get_job_name
