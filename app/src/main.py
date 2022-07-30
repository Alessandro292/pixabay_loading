import uvicorn

from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import JSONResponse

from app.src.connection.connection_minio import MinioClient
from app.src.connection.connection_mysql import MySQLClient
from app.src.constants.entities import AnimalEntity, LanguageEntity

from app.src.services.services import count_flow, download_flow

app = FastAPI(
    title="Pixabay Loading",
    description='Target of the demo is to download images and extract useful metadata from Pixabay'
)

router = APIRouter(
    prefix="/pixabay",
    dependencies=[],
    responses={}
)

@router.get("/download", tags=["Download"])
async def download_images(
    *,
    minio_client: MinioClient = Depends(MinioClient.init_client),
    mysql_client: MySQLClient = Depends(MySQLClient.init_client),
    animal: AnimalEntity,
    lang: LanguageEntity,
    images_number: int
):

    status_code, output = download_flow(mysql_client=mysql_client,
                                        minio_client=minio_client,
                                        animal=animal.value,
                                        lang=lang.value,
                                        images_number=images_number)

    return JSONResponse(status_code=status_code, content=output)


@router.get("/count", tags=["Count"])
async def count_images(
    *,
    mysql_client: MySQLClient = Depends(MySQLClient.init_client)
):

    status_code, output = count_flow(mysql_client=mysql_client)

    return JSONResponse(status_code=status_code, content=output)

# Including FastAPI Router
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config="./config/logging.conf")