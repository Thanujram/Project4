from sqlalchemy import Table, Column, Integer, String
from config.db import meta

images = Table(
    'image',meta,
    Column('id',Integer,primary_key=True),
    Column('url',String(255)),
    Column('name',String(255)),
    Column('type',String(255))
)