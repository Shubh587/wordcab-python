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

"""Live client feature to communicate with a websocket endpoint."""

import logging
from typing import Optional, Union

import websockets

from wordcab.login import get_token

logger = logging.getLogger(__name__)


class LiveClient:
    """Wordcab API LiveClient used to transcribe audio in real-time."""

    def __init__(
        self, server_url: str, source_lang: str, api_key: Union[str, None] = None
    ) -> None:
        """Initialize LiveClient."""
        self.server_url = server_url
        if "ws://" not in self.server_url:
            raise ValueError(
                "Expected server_url to be a websocket URL."
                "Example: ws://localhost:5001/api/v1/live\n"
                f"But got: {self.server_url}"
            )

        self.source_lang = source_lang

        if api_key is None:
            self.api_key = get_token()
        else:
            self.api_key = api_key

        if self.api_key is None:
            raise ValueError(
                "API Key not found. You must set the WORDCAB_API_KEY environment"
                " variable. Use `wordcab login` to loginto the Wordcab CLI and set the"
                " environment variable."
            )

    async def __aenter__(self) -> "LiveClient":
        """Enter the live client context."""
        self.websocket = await websockets.connect(
            f"{self.server_url}?source_lang={self.source_lang}"
        )
        return self

    async def __aexit__(
        self,
        exception_type: Optional[Union[ValueError, TypeError, AssertionError]],
        exception_value: Optional[Exception],
        traceback: Optional[Exception],
    ) -> None:
        """Exit the live client context."""
        await self.websocket.close()

    async def send_audio(self, audio_data: bytes) -> str:
        """Send audio data to the websocket endpoint."""
        await self.websocket.send(audio_data)

        response = await self.websocket.recv()

        return response
