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

"""Test suite for the Client get_stats method."""

from wordcab.client import Client
from wordcab.core_objects import Stats


def test_get_stats(api_key: str) -> None:
    """Test client get_stats method."""
    with Client(api_key=api_key) as client:
        stats = client.get_stats(min_created="2021-01-01", max_created="2021-01-31")
        assert isinstance(stats, Stats)
        assert hasattr(stats, "account_email")
        assert hasattr(stats, "plan")
        assert hasattr(stats, "monthly_request_limit")
        assert hasattr(stats, "request_count")
        assert hasattr(stats, "minutes_summarized")
        assert hasattr(stats, "transcripts_summarized")
        assert hasattr(stats, "metered_charge")
        assert hasattr(stats, "min_created")
        assert stats.min_created == "2021-01-01T00:00:00"
        assert hasattr(stats, "max_created")
        assert stats.max_created == "2021-01-31T00:00:00"
        assert hasattr(stats, "tags")
        assert stats.tags is None
