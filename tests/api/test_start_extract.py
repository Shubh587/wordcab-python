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

"""Test suite for the API start_extract function."""

from pathlib import Path

from wordcab.api import start_extract
from wordcab.core_objects import ExtractJob, GenericSource, JobSettings


def test_api_start_extract(api_key: str) -> None:
    """Test the start_extract function."""
    source_object = GenericSource(filepath=Path("tests/sample_1.txt"))
    job = start_extract(
        source_object=source_object,
        display_name="test-extract-api",
        pipelines=["emotions"],
        api_key=api_key,
    )
    assert isinstance(job, ExtractJob)
    assert job.display_name == "test-extract-api"
    assert job.job_name is not None
    assert job.source == "generic"
    assert job.settings == JobSettings(
        ephemeral_data=False,
        pipeline="emotions",
        split_long_utterances=False,
        only_api=True,
    )
