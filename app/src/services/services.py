import io
import logging
import requests

from fastapi import status
from typing import Any

from app.src.connection.connection_minio import MinioClient
from app.src.connection.connection_mysql import MySQLClient
from app.src.config.variables import PIXABAY_API_KEY, PIXABAY_URL
from app.src.services.utils.utility_functions import image_metadata, build_json

logger = logging.getLogger(__name__)


def get_flow(mysql_client: MySQLClient, minio_client: MinioClient, animal: str, lang: str, images_number: int) -> [int, Any]:
    """
    Service related to /pixabay/download path operation

    """

    if (images_number < 3 or images_number > 200):

        # check input: Pixabay does not accept a number less then 3 and greater then 200

        content = "Input images_number not valid: please insert a number between 3 and 200."
        logger.error(content)
        return status.HTTP_422_UNPROCESSABLE_ENTITY, content

    elif(PIXABAY_API_KEY=='<YOUR_API_KEY>'):

        # Check pixabay key

        content = "Pixabay key not valid: you forgot to replace the variable PIXABAY_API_KEY with <YOUR_API_KEY>"
        logger.error(content)
        return status.HTTP_422_UNPROCESSABLE_ENTITY, content

    else:

        logger.info("Input images_number valid")

        images_inserted = []

        filter_images_url = f"{PIXABAY_URL}?key={PIXABAY_API_KEY}&q={animal}&image_type=photo&lang={lang}&order=latest&page=1&per_page={images_number}"

        r = requests.get(filter_images_url, stream=True)

        if r.status_code == 200:
            # getting 20 url of images from the previous url
            series_images_url = [json['previewURL'] for json in r.json()['hits']]

            # check if exist Bucket
            minio_client.check_bucket()

            # download images
            for image_url in series_images_url:
                filename = image_url.split("/")[-1]

                r = requests.get(image_url, stream=True)
                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True

                    minio_client.put_object(object_name=filename,
                                            content=io.BytesIO(r.content),
                                            length=len(r.content))

                    json_object, tupla_sql = image_metadata(image_name=filename, animal=animal,
                                                                       lang=lang, image_bytes=r.content)

                    minio_client.put_object(object_name=f'{filename.split(".")[0]}.json',
                                            content=io.BytesIO(json_object.encode()),
                                            length=len(json_object.encode()))

                    mysql_client.insert_db(val=tupla_sql)
                    mysql_client.commit_db()

                    images_inserted.append(True)
                    logger.info('Image sucessfully Downloaded: ', filename)

                else:

                    images_inserted.append(False)
                    logger.error('Image Couldn\'t be retreived')

            images_loaded = len(list(filter(lambda e: e == True, images_inserted)))

            content = f"Images inserted correctly: {images_loaded}"

            return r.status_code, content

        else:

            # return status code not equal to 200
            return r.status_code, r.content.decode("utf-8")


def count_flow(mysql_client: MySQLClient) -> [int, Any]:

    count_animal = mysql_client.group_and_count_db(field="animal")

    output_json = build_json(count_animal=count_animal)

    return status.HTTP_200_OK, output_json


def download_flow(minio_client: MinioClient, file_name: str):

    data = minio_client.get_object(file_name=file_name)

    return status.HTTP_200_OK, data