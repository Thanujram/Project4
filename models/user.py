from sqlalchemy import Table, Column, MetaData, Integer, String
from config.db import meta

users = Table(
    'user',meta,
    Column('id',Integer,primary_key=True),
    Column('username',String(255)),
    Column('password',String(255)),
    Column('email',String(255))
)