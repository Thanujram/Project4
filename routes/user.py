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
from matplotlib import pyplot as plt
from pathlib import Path
from PIL import Image as pim
# import string

import cv2
# import mat as plt
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
async def uploadimage(file: UploadFile, response: Response):

    print(file.content_type);
    #image/bmp, image/jpeg, image/x-png; image/png, or image/gif
    if(file.content_type == "image/jpg" or file.content_type == "image/jpeg" or file.content_type == "image/png"):
        path = r'C:\Users\jasit\Desktop\Project4\New folder'
        save_path = os.path.join(path, file.filename)

        try:
            veri_img = pim.open(file.file)
            veri_img.verify()
        except Exception as er:
            print(er)
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                'message': 'File is currupted'
            }

        try:
            file_object = await file.read()

            with open(save_path, 'wb') as buffer:
                buffer.write(file_object)
            await file.close()

        except Exception as er:
            print(er)

        conn.execute(images.insert().values(
            url=save_path,
            name=file.filename
        ))
        return {'filename': file.filename}

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'message': 'File type not supporting'
        }


@user.get("/classification")
async def classify(filename: str, response: Response):

    if filename is None:
        response.status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        return {'message': 'NO URL'}

    image_fetched: Image = conn.execute(images.select().where(images.c.name == filename)).fetchone()

    if image_fetched is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {'message': 'No image'}

    result = classify(image_fetched.url)

    return result

# Function for classifing
def classify(url: str):

    img = cv2.imread(url)

    # To check the image loading
    # plt.imshow(img)
    # plt.show()

    # Model trained should be loaded here
    # result = predict(img)

    # Value for URL temp
    result = {
        'result': url
    }

    return (result)

