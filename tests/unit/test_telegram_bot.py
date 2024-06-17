import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from telegram_bot import send_photo, get_updates, send_document, get_constants


class TestTelegramBot(unittest.TestCase):

    @patch('telegram_bot.requests.post')
    def test_send_photo(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        # Mocking the file opening
        photo_path = 'dummy_photo.jpg'
        with patch('builtins.open', mock_open(read_data='data')) as mock_file:
            chat_id = '123456'
            caption = 'Test Caption'
            response = send_photo(chat_id, caption, photo_path)

            # Asserting the API call
            self.assertTrue(response['ok'])
            mock_post.assert_called_once()
            mock_file.assert_called_once_with(photo_path, 'rb')

    @patch('telegram_bot.requests.get')
    def test_get_updates(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True, "result": []}
        mock_get.return_value = mock_response

        response = get_updates()

        # Asserting the API call
        self.assertTrue(response['ok'])
        mock_get.assert_called_once()

    @patch('telegram_bot.requests.post')
    def test_send_document(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True}
        mock_post.return_value = mock_response

        # Mocking the file opening
        document_path = 'dummy_document.txt'
        with patch('builtins.open', mock_open(read_data='data')) as mock_file:
            chat_id = '123456'
            response = send_document(chat_id, document_path)

            # Asserting the API call
            self.assertTrue(response['ok'])
            mock_post.assert_called_once()
            mock_file.assert_called_once_with(document_path, 'rb')

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "dummy_token"})
    def test_get_constants(self):
        TELEGRAM_BASE_URL, TOKEN = get_constants()
        self.assertEqual(TELEGRAM_BASE_URL, 'https://api.telegram.org/bot')
        self.assertEqual(TOKEN, 'dummy_token')


if __name__ == '__main__':
    unittest.main()
