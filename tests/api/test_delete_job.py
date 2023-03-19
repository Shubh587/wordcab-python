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

"""Test suite for the API delete_job function."""

from wordcab.api import delete_job


def test_api_delete_job(api_key: str) -> None:
    """Test the delete_job function."""
    deleted_job = delete_job(
        job_name="job_aLt5gw5AZwg2rnqaqR46kB7csMfwqTdB", api_key=api_key
    )
    assert deleted_job is not None
    assert isinstance(deleted_job, dict)
    assert deleted_job["job_name"] == "job_aLt5gw5AZwg2rnqaqR46kB7csMfwqTdB"
