import io
import json
import logging
from PIL import Image

logger = logging.getLogger(__name__)

def image_metadata(image_name: str, animal: str, lang: str, image_bytes: bytes) -> str:

    image = Image.open(io.BytesIO(image_bytes))

    info_dict = {
        "Filename": image_name,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    json_object = json.dumps(info_dict)

    # Build tupla used for inserting row in db

    tupla_sql = (image_name, animal, lang,
                 image.format, image.mode,
                 getattr(image, "n_frames", 1), image.height, image.width,
                 getattr(image, "is_animated", False))

    return json_object, tupla_sql


def build_json(**kwargs) -> dict:

    dictionary = {}

    for key, tuple_list in kwargs.items():
        dictionary[key] = [{t[0]: t[1]} for t in tuple_list]

    return dictionary
