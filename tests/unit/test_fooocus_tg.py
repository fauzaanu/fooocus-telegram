import json
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from fooocus_tg import get_styles_file, monitor_folders, send_to_telegram, delete_local


class TestFooocusTG(unittest.TestCase):

    @patch('fooocus_tg.Image.open')
    def test_get_styles_file(self, mock_image_open):
        # Create a mock image with metadata
        mock_image = MagicMock()
        mock_image.info = {
            "parameters": json.dumps({
                "seed": "12345",
                "full_negative_prompt": ["negative_prompt_example"],
                "full_prompt": ["prompt_example"]
            })
        }
        mock_image_open.return_value = mock_image

        file_path = "dummy_image.png"
        styles_json, seed = get_styles_file(file_path)

        expected_styles = json.dumps([{
            "name": "12345_original",
            "prompt": "prompt_example",
            "negative_prompt": "negative_prompt_example"
        }])
        self.assertEqual(styles_json, expected_styles)
        self.assertEqual(seed, "12345")

    @patch('fooocus_tg.os.walk')
    @patch('fooocus_tg.get_styles_file')
    @patch('fooocus_tg.send_to_telegram')
    @patch('fooocus_tg.delete_local')
    def test_monitor_folders(self, mock_delete_local, mock_send_to_telegram, mock_get_styles_file, mock_os_walk):
        mock_os_walk.return_value = [
            ('/', ('subdir',), ('image1.png', 'image2.jpg'))
        ]
        mock_get_styles_file.return_value = ("dummy_styles_json", "dummy_seed")
        mock_send_to_telegram.return_value = True
        mock_delete_local.return_value = True

        with patch.dict(os.environ, {"FOCUS_OUTPUT_FOLDER": "/"}):
            processed_count = monitor_folders()
            self.assertEqual(processed_count, 2)

    @patch('fooocus_tg.send_photo')
    @patch('fooocus_tg.send_document')
    @patch('builtins.open', new_callable=mock_open)
    @patch('fooocus_tg.os.remove')
    def test_send_to_telegram(self, mock_os_remove, mock_open, mock_send_document, mock_send_photo):
        mock_send_photo.return_value = {"ok": True}
        mock_send_document.return_value = {"ok": True}

        with patch.dict(os.environ, {"TELEGRAM_CHAT_ID": "dummy_chat_id"}):
            result = send_to_telegram("dummy_image_path", "dummy_styles_json", "dummy_seed")

            self.assertTrue(result)
            mock_open.assert_called_once_with("dummy_seed.json", "w")
            mock_send_photo.assert_called_once()
            mock_send_document.assert_called_once()
            mock_os_remove.assert_called_once_with("dummy_seed.json")

    @patch('fooocus_tg.os.remove')
    def test_delete_local(self, mock_os_remove):
        image_path = "dummy_image.png"
        result = delete_local(image_path)
        self.assertTrue(result)
        mock_os_remove.assert_called_once_with(image_path)


if __name__ == '__main__':
    unittest.main()
