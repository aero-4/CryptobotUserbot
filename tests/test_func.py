import re

import pytest
from unittest.mock import AsyncMock, patch

from main import check_exist, client, validation


def validation(text: str):
    if not text or not isinstance(text, str):
        return None

    URL_PATTERN = re.compile(r"(?:https?://)?t\.me/send\?start=([^&\s]*)")
    current = re.search(URL_PATTERN, text)
    if current is not None:
        return current.group(1)
    return None



class FakeResponse:
    def __init__(self, text):
        self.text = text


class FakeConversation:
    def __init__(self):
        self.sent_message = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def send_message(self, message):
        self.sent_message = message

    async def get_response(self):
        return FakeResponse("TEST RESPONSE")


@pytest.mark.parametrize("test_input,expected", [
    ("Привет! Проверь ссылку: https://t.me/send?start=DsOPCZUidas987 и действуй.", "DsOPCZUidas987"),
    ("Привет! Проверь ссылку: http://t.me/send?start=DsOPCZUidas987 и действуй.", "DsOPCZUidas987"),
    ("Привет! Проверь ссылку: t.me/send?start=DsOPCZUidas987 и действуй.", "DsOPCZUidas987"),
    ("Привет! Проверь ссылку: https://t.me/send?start= и действуй.", ""),
    ("Привет! Здесь нет ссылки для проверки.", None),
    ("Привет! Проверь ссылку: https://t.me/send?start=DsOPCZUidas987&ref=abc и действуй.", "DsOPCZUidas987"),
])
def test_validation(test_input, expected):
    assert validation(test_input) == expected


@pytest.mark.asyncio
async def test_check_exist_no_link():
    test_msg = "Привет! Здесь нет ссылки для проверки."

    with patch.object(client, '__call__', new=AsyncMock()) as mock_unblock:
        with patch.object(client, 'conversation', return_value=FakeConversation()) as mock_conv:
            await check_exist(test_msg)

            mock_conv.assert_not_called()
            mock_unblock.assert_not_called()
