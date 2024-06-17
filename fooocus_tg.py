"""
Fooocus_tg is a script that monitors the output folder of fooocus and sends the images to telegram
todo: delete the log file without causing fooocus problems.
( perheps its writing the log file while we delete it and causes a crash)
"""
import json
import os
import time

from PIL import Image
from dotenv import load_dotenv

from telegram_bot import send_photo, send_document


def get_styles_file(file_path: str):
    """Get the styles from the file"""
    img = Image.open(file_path)
    metadata = img.info

    try:
        parmeters_str = metadata["parameters"]
        json_parameters = json.loads(parmeters_str)

        seed = json_parameters["seed"]
        full_negative_prompt = json_parameters["full_negative_prompt"]
        full_prompt = json_parameters["full_prompt"]
    except KeyError:
        seed = "PLEASE_ENABLE_METADATA_WITH_FOOOCUS"
        full_negative_prompt = ["unknown"]
        full_prompt = ["unknown"]

    this_style = {
        "name": seed + "_original",
        "prompt": ",".join(full_prompt),
        "negative_prompt": ",".join(full_negative_prompt)
    }

    # remove metadata from the image before sending to telegram
    # metadata is removed when downloaded from telegram, however if it changes in the future
    # this will ensure that the metadata is removed
    img.save(file_path, exif=b'')
    json_combined_object = json.dumps([this_style])
    return json_combined_object, seed


def monitor_folders():
    """Monitors all focus output folders and sends the images to telegram and deletes them locally"""
    output_folder = os.getenv("FOCUS_OUTPUT_FOLDER")
    count_processed = 0

    if not os.path.exists(output_folder):
        return None
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".webp"):
                file = os.path.join(root, file)
                styles, seed = get_styles_file(file)
                send_to_telegram(file, styles, seed)
                delete_local(file)
                count_processed += 1
    return count_processed


def send_to_telegram(image_path: str, styles_json: str, seed: str):
    """Send the images to telegram"""
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    send_photo(CHAT_ID,
               seed,
               image_path)
    styles_json_path = f"{seed}.json"
    with open(styles_json_path, "w") as f:
        f.write(styles_json)
    send_document(CHAT_ID, styles_json_path)
    os.remove(styles_json_path)
    return True


def delete_local(image_path: str):
    """Delete the images locally"""
    os.remove(image_path)
    return True


if __name__ == "__main__":
    while True:

        load_dotenv(override=True)

        try:
            timeout = int(os.getenv("FTG_TIMEOUT", 20))
        except ValueError:
            timeout = 20

        print("Monitoring the folders")
        print("Timeout: 20 seconds")
        procssed = monitor_folders()
        if procssed == 0:
            time.sleep(20)  # taking a break for a minute if no files are found

