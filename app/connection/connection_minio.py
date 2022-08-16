import logging
from minio import Minio

from app.config.variables import MINIO_USER, MINIO_BUCKET, MINIO_ENDPOINT, MINIO_PASSWORD

logger = logging.getLogger(__name__)


class MinioClient:

    def __init__(self, minio_session: Minio):
        """
        Init MinioClient

        :param minio_session:
            Minio object which is responsible for calling Minio API

        """

        self.__minio_session = minio_session

    @staticmethod
    def init_client():
        """
        Static method used for initializing Minio Client

        """

        minio_session = Minio(endpoint=MINIO_ENDPOINT,
                                access_key=MINIO_USER,
                                secret_key=MINIO_PASSWORD,
                                secure=False)

        return MinioClient(minio_session)

    def check_bucket(self):

        found = self.__minio_session.bucket_exists(MINIO_BUCKET)

        if not found:
            self.__minio_session.make_bucket(MINIO_BUCKET)
        else:
            logger.info(f"Minio Bucket {MINIO_BUCKET} already exists")

    def put_object(self, object_name: str, content: bytes, length: int) -> None:

        self.__minio_session.put_object(bucket_name=MINIO_BUCKET,
                                        object_name=object_name,
                                        data=content,
                                        length=length)

    def get_object(self, file_name: str) -> bytes:

        logger.info(f"Try to retrieve object {file_name} from {MINIO_BUCKET} bucket")

        blob = self.__minio_session.get_object(bucket_name=MINIO_BUCKET,
                                               object_name=file_name)

        return blob.data

    def list_images(self):

         objects_list = list(self.__minio_session.list_objects(bucket_name=MINIO_BUCKET))

         images_name = [obj.object_name for obj in objects_list if 'jpg' in obj.object_name]

         return images_name