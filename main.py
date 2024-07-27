from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
import boto3
from botocore.client import Config
from contextlib import asynccontextmanager
from io import BytesIO

from database import create_tables, drop_tables
from router import router as memes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    # await drop_tables()



app = FastAPI(lifespan=lifespan)
app.include_router(memes_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)