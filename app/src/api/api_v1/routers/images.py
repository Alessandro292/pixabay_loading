import logging

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.src.connection.connection_minio import MinioClient
from app.src.connection.connection_mysql import MySQLClient
from app.src.constants.entities import AnimalEntity, LanguageEntity

from app.src.services.images_services import  counting_service, download_service, getting_service, listing_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/pixabay",
    tags=["images"],
    dependencies=[],
    responses={},
)

@router.get("/download", tags=["images"])
async def download_pixabay_images(
    *,
    minio_client: MinioClient = Depends(MinioClient.init_client),
    mysql_client: MySQLClient = Depends(MySQLClient.init_client),
    animal: AnimalEntity,
    lang: LanguageEntity,
    images_number: int
):

    status_code, output = download_service(mysql_client=mysql_client,
                                            minio_client=minio_client,
                                            animal=animal.value,
                                            lang=lang.value,
                                            images_number=images_number)

    return JSONResponse(status_code=status_code, content=output)


@router.get("/counting", tags=["images"])
async def counting_animals(
    *,
    mysql_client: MySQLClient = Depends(MySQLClient.init_client)
):

    status_code, output = counting_service(mysql_client=mysql_client)

    return JSONResponse(status_code=status_code, content=output)


@router.get("/listing", tags=["images"])
async def listing_images(
        *,
        minio_client: MinioClient = Depends(MinioClient.init_client)
):

    status_code, output = listing_service(minio_client=minio_client)

    return JSONResponse(status_code=status_code, content=output)


@router.get("/getting", tags=["images"])
async def getting_content(
    *,
    minio_client: MinioClient = Depends(MinioClient.init_client),
    file_name: str
):

    status_code, output = getting_service(minio_client=minio_client, file_name=file_name)

    return Response(content=output, status_code=status_code, media_type='image/jpeg')
