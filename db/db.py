from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser

conf = ConfigParser()
# 读取配置文件
conf.read('config.ini')

db_host = conf.get('db', 'host')
db_user = conf.get('db', 'user')
db_password = conf.get('db', 'password')
db_name = conf.get('db', 'db')

DB_URI = f'mysql+pymysql://{db_user}:{db_password}@{db_password}/{db_name}'
engine = create_engine(DB_URI, pool_recycle=3600)
DBSession = sessionmaker(bind=engine)
session = DBSession()
