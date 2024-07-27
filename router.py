from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query, Path
from fastapi.responses import JSONResponse, StreamingResponse
import boto3
from botocore.client import Config
from io import BytesIO

from repository import MemeRepository
from schemas import MemeAdd

router = APIRouter(
    prefix="/memes",
    tags=["Мемы"]
)

minio_url = 'http://minio:9000'
access_key = 'admin'
secret_key = 'password'


s3_client = boto3.client('s3',
                         endpoint_url=minio_url,
                         aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key,
                         config=Config(signature_version='s3v4'))
bucket_name = 'memes'

try:
    s3_client.create_bucket(Bucket=bucket_name)
except s3_client.exceptions.BucketAlreadyOwnedByYou:
    pass

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Неправильный тип файла. Необходима картинка jpeg/png")
    file_content = await file.read()
    s3_client.put_object(Bucket=bucket_name, Key=file.filename, Body=file_content)
    meme_data = MemeAdd(name=file.filename)
    meme_id = await MemeRepository.add_one(meme_data)
    return JSONResponse(status_code=200, content={"Добавлен": file.filename})

@router.delete("/{meme_id}")
async def delete_file(meme_id: int):
    meme = await MemeRepository.find_by_id(meme_id)
    if not meme:
        raise HTTPException(status_code=404, detail="Мем не найден")
    s3_client.delete_object(Bucket=bucket_name, Key=meme.name)
    await MemeRepository.delete_by_id(meme_id)
    return JSONResponse(status_code=200, content={"Удалён": meme.name})

@router.get("")
async def get_memes(limit: int = Query(2, gt=0, le=100), offset: int = Query(0, ge=0)):
    memes = await MemeRepository.find_all(limit=limit, offset=offset)
    return {"Мемы": memes}

@router.get("/{meme_id}")
async def get_meme(meme_id: int):
    meme = await MemeRepository.find_by_id(meme_id)
    if not meme:
        raise HTTPException(status_code=404, detail="Мем не найден")
    filename = meme.name
    file_obj = s3_client.get_object(Bucket=bucket_name, Key=filename)
    file_stream = file_obj['Body'].read()
    return StreamingResponse(BytesIO(file_stream), media_type='image/jpeg')


@router.put("/{meme_id}")
async def update_meme(meme_id: int = Path(..., ge=1), file: UploadFile = File(None), new_name: str = None):
    meme = await MemeRepository.find_by_id(meme_id)
    if not meme:
        raise HTTPException(status_code=404, detail="Мем не найден")

    if not file and not new_name:
        raise HTTPException(status_code=400, detail="Необходимо ввести новое имя файла или сам файл для обновления")

    if file:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Неправильный тип файла. Необходима картинка jpeg/png")
        file_content = await file.read()
        s3_client.put_object(Bucket=bucket_name, Key=file.filename, Body=file_content)

        s3_client.delete_object(Bucket=bucket_name, Key=meme.name)

        meme.name = file.filename
        await MemeRepository.update_meme(meme_id, meme.name)

    elif new_name:
        s3_client.copy_object(Bucket=bucket_name,
                              CopySource={'Bucket': bucket_name, 'Key': meme.name},
                              Key=new_name)
        s3_client.delete_object(Bucket=bucket_name, Key=meme.name)

        meme.name = new_name
        await MemeRepository.update_meme(meme_id, meme.name)

    return JSONResponse(status_code=200, content={"Обновлён мем с id": meme_id, "Имя": meme.name})

# @router.get("/memes/")
# async def get_memes():
#     response = s3_client.list_objects_v2(Bucket=bucket_name)
#     if 'Contents' not in response:
#         return JSONResponse(status_code=200, content={"memes": []})
#     memes = [{"filename": item['Key']} for item in response['Contents']]
#     return JSONResponse(status_code=200, content={"memes": memes})

