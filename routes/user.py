import os.path
import shutil
from mimetypes import MimeTypes
from tokenize import String
from typing import Annotated

from fastapi import APIRouter, UploadFile, status, Response, File
import time

from config.db import conn
from models.index import users, images
from schemas.index import User, Image

from pathlib import Path
# import string

import cv2
user = APIRouter()

# Login
@user.post("/login")
async def login(user: User, response:Response):
    if (user.username is None or user.password is None):
        response.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        return {'message':'No credentials'}

    user_au: User = conn.execute(users.select().where(users.c.username == user.username)).fetchone();

    if user_au is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {'message':'No user account'}
    elif user_au.password == user.password:
        return {'token': user_au.username,
                'user':{
                    'name' : user_au.username
                }
                }
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message':'Credintials not matching'}

# Register
@user.post("/register")
async def register(user: User, response: Response):
    if (user.username is None or user.password is None):
        response.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        return {'message':'No credentials'}

    user_au: User = conn.execute(users.select().where(users.c.username == user.username)).fetchone()

    if user_au is None:
        conn.execute(users.insert().values(
            username=user.username,
            password=user.password
        ))
        return {'token': user.username,
                'user':{
                    'name' : user.username
                }
                }
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message':'Already Exists'}

@user.post("/upload")
async def uploadimage(file: UploadFile):

    # if(file.validate())

    path = r'C:\Users\HP\PycharmProjects\New folder\images'
    save_path = os.path.join(path,file.filename)

    try:
        file_object = await file.read()

        with open(save_path,'wb') as buffer:
            buffer.write(file_object)
        await file.close()

    except Exception as er:
        print(er)


    # path = r'C:\Users\HP\PycharmProjects\New folder\images'
    # file_name = file.filename
    # cv2.imwrite(os.path.join(path,filename), file.)
    # cv2.waitKey(0)

    # img = cv2.imread(file.file)
    # cv2.imshow("Image",img)


    conn.execute(images.insert().values(
        url=save_path,
        name=file.filename
    ))



    return {'filename':file.filename}

@user.post("/classification")
async def classify(imagename: str, response: Response):

    if imagename is None:
        response.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        return {'message': 'No credentials'}

    image_fetched: Image = conn.execute(images.select().where(images.c.url == imagename)).fetchone()

    if image_fetched is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {'message': 'No image'}

    result = classify(image_fetched.url)

    return {
        'result':result
    }
def classify(url: str):
    result = url
    return (result)

# pip install python-multipart
# Login
# @user.get("/login/{username}/{password}")
# async def login(username: str, password: str):
#     user_au: User
#     user_au = conn.execute(users.select().where(users.c.username == username)).fetchone();
#     if user_au.password == password:
#         return {'Auth': 'Grant'}
#     else:
#         return {'Auth':'NO'}
# @user.get("/")
# async def read_data():
#     return conn.execute(users.select()).fetchall()
#
# @user.get("/{id}")
# async def read_data(id: int):
#     return conn.execute(users.select().where(users.c.id == id)).fetchall()
#
# @user.post("/register/{username}/{password}")
# async def register(username: str, password: str):
#
#
# @user.post("/")
# async def write_data(user: User):
#     conn.execute(users.insert().values(
#         username = user.username,
#         password = user.password
#     ))
#     return conn.execute(users.select()).fetchall()

# image = file.read(file.size)
    #
    # obj = DriveAPI()
    # obj.FileUpload(image,file.filename)
    # obj.FileUpload()FileUpload(self=DriveAPI.FileUpload,image=image,name=file.filename)

# path: Path = r'C:\Users\HP\PycharmProjects\New folder\images'
#
# try:
#     with path.open("wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#         print("Saved")
# finally:
#     file.file.close()