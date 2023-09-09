from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:1234@127.0.0.2:3306/project3")
meta = MetaData()
conn = engine.connect()