"""Test the LiveClient class."""

from unittest.mock import AsyncMock, patch

import pytest
import websockets
from wordcab.live import LiveClient


class TestLiveClient:
    """Test the LiveClient class."""

    @pytest.mark.usefixtures("api_key")
    def test_initialization(self, api_key) -> None:
        """Test initialization."""
        client = LiveClient("ws://localhost:5001/api/v1/live", "en", api_key=api_key)

        assert client.server_url == "ws://localhost:5001/api/v1/live"
        assert client.source_lang == "en"
        assert client.api_key == api_key

    def test_initialization_bad_url(self) -> None:
        """Test initialization with a bad URL."""
        with pytest.raises(ValueError) as exc:
            LiveClient("http://localhost:5001/api/v1/live", "en")

        assert "Expected server_url to be a websocket URL" in str(exc.value)

    def test_initialization_missing_api_key(self) -> None:
        """Test initialization with a missing API key."""
        with patch("wordcab.live.get_token", return_value=None):
            with pytest.raises(ValueError) as exc:
                LiveClient("ws://localhost:5001/api/v1/live", "en")

            assert "API Key not found" in str(exc.value)

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("api_key")
    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_context_entry_and_exit(self, mock_connect, api_key) -> None:
        """Test context entry and exit."""
        mock_websocket = AsyncMock(spec=websockets.WebSocketClientProtocol)
        mock_connect.return_value = mock_websocket

        async with LiveClient(
            "ws://localhost:5001/api/v1/live", "en", api_key=api_key
        ) as client:
            assert client.websocket is not None

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("api_key")
    async def test_send_audio(self, api_key) -> None:
        """Test send_audio."""
        audio_data = b"some_audio_data"
        expected_response = "response_data"

        mock_websocket = AsyncMock(spec=websockets.WebSocketClientProtocol)
        mock_websocket.recv.return_value = expected_response

        with patch(
            "wordcab.live.websockets.connect",
            new_callable=AsyncMock,
            return_value=mock_websocket,
        ) as mocked_connect:
            async with LiveClient(
                "ws://localhost:5001/api/v1/live", "en", api_key=api_key
            ) as client:
                response = await client.send_audio(audio_data)
                mocked_connect.assert_called_once_with(
                    "ws://localhost:5001/api/v1/live?source_lang=en"
                )
                client.websocket.send.assert_called_once_with(audio_data)
                client.websocket.recv.assert_called_once()

                assert response == expected_response
