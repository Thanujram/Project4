from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:12345678@127.0.0.1:3306/trendy_techs")
meta = MetaData()
conn = engine.connect()