import uvicorn

from fastapi import FastAPI

from app.src.api import main_router

app = FastAPI(
    title="Pixabay Loading",
    description='Target of the demo is to download images and extract useful metadata from Pixabay',
    contact={
        "Name": "Alessandro Impagnatiello"
    },
    version="1.0"
)


app.include_router(router=main_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config="./config/logging.conf")