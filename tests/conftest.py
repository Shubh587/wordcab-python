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

"""Fixtures and mocks for all test files."""

import random
from pathlib import Path
from typing import List, Optional

import pytest
import responses
from wordcab.client import Client
from wordcab.core_objects import AudioSource, BaseSource, GenericSource, InMemorySource


@pytest.fixture
def mock_server():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def api_key() -> Optional[str]:
    """Fixture for the API key."""
    return "".join(random.choice("abcdef1234567890") for _ in range(32))


@pytest.fixture
def client() -> Client:
    """Client fixture."""
    return Client(api_key="dummy_api_key")


@pytest.fixture
def get_job_name() -> str:
    """Fixture for a job name."""
    return f"job_{random.randint(1000000000, 9999999999)}"


@pytest.fixture
def get_transcript_id() -> str:
    """Fixture for a transcript id."""
    return f"generic_transcript_{random.randint(1000000000, 9999999999)}"


@pytest.fixture
def in_memory_source() -> InMemorySource:
    """Fixture for an InMemorySource object."""
    with open("tests/sample_1.txt", "rb") as f:
        file = f.read()
    obj = {"transcript": file.decode("utf-8").splitlines()}
    return InMemorySource(obj=obj)


@pytest.fixture
def generic_source_txt() -> GenericSource:
    """Fixture for a GenericSource object."""
    return GenericSource(filepath=Path("tests/sample_1.txt"))


@pytest.fixture
def generic_source_json() -> GenericSource:
    """Fixture for a GenericSource object."""
    return GenericSource(filepath=Path("tests/sample_1.json"))


@pytest.fixture
def generic_url_json() -> GenericSource:
    """Fixture for a GenericSource object."""
    return GenericSource(
        url="https://raw.githubusercontent.com/Wordcab/wordcab-python/main/tests/sample_1.json"
    )


@pytest.fixture
def audio_source() -> AudioSource:
    """Fixture for an AudioSource object."""
    return AudioSource(filepath=Path("tests/sample_1.mp3"))


@pytest.fixture
def audio_url_source() -> AudioSource:
    """Fixture for an AudioSource object."""
    return AudioSource(
        url="https://github.com/Wordcab/wordcab-python/blob/main/tests/sample_1.mp3?raw=true"
    )


@pytest.fixture
def base_source() -> BaseSource:
    """Fixture for a wrong BaseSource object."""
    return BaseSource(filepath=Path("tests/sample_1.txt"))


@pytest.fixture
def context_elements() -> List[str]:
    """Fixture for a list of context elements."""
    return ["keywords", "issue", "purpose", "discussion_points", "next_steps"]
