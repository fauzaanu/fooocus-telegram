import os

import requests
from dotenv import load_dotenv


def send_photo(chat_id, caption, photo):
    """Sending the photos with spoilers"""
    TELEGRAM_BASE_URL, TOKEN = get_constants()
    url = f'{TELEGRAM_BASE_URL}{TOKEN}/sendPhoto'

    caption = f"```seed {caption}```"

    with open(photo, 'rb') as photo:
        # multipart/form-data
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': 'MarkdownV2',
        }
        files = {
            'photo': photo,
        }
        response = requests.post(url, data=data, files=files)
        return response.json()


def get_constants():
    TELEGRAM_BASE_URL = 'https://api.telegram.org/bot'
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    return TELEGRAM_BASE_URL, TOKEN


def get_updates():
    """Just to test requests"""
    TELEGRAM_BASE_URL, TOKEN = get_constants()
    url = f'{TELEGRAM_BASE_URL}{TOKEN}/getUpdates'
    response = requests.get(url)
    return response.json()


def send_document(chat_id, document):
    """Sending the documents with spoilers"""
    TELEGRAM_BASE_URL, TOKEN = get_constants()
    url = f'{TELEGRAM_BASE_URL}{TOKEN}/sendDocument'

    with open(document, 'rb') as document:
        # multipart/form-data
        data = {
            'chat_id': chat_id,
        }
        files = {
            'document': document,
        }
        response = requests.post(url, data=data, files=files)
        return response.json()


if __name__ == '__main__':
    pass
