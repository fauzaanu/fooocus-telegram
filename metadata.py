"""
This is a file that was used to test if the metadata got removed, code is kept only for future reference
"""
import json

from PIL import Image

if __name__ == "__main__":
    img = Image.open("2024-06-17_07-01-15_2838.png")
    metadata = img.info

    parmeters_str = metadata["parameters"]
    json_parameters = json.loads(parmeters_str)
    with open("parameters.json", "w") as f:
        json.dump(json_parameters, f)

    seed = json_parameters["seed"]
    full_negative_prompt = json_parameters["full_negative_prompt"]
    full_prompt = json_parameters["full_prompt"]

    this_style = {
        "name": seed + "_original",
        "prompt": ",".join(full_prompt),
        "negative_prompt": ",".join(full_negative_prompt)
    }

    # remove metadata from the image
    img.save("2024-06-17_07-01-15_2838_r.png", exif=b'')
    img = Image.open("2024-06-17_07-01-15_2838_r.png")
    print("after saving", img.info)