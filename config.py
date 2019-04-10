from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class BaseConfig:
    LOG_LEVEL = 'DEBUG'
    REDIS_HOST = '0.0.0.0'
    REDIS_PORT = 6379
    SQLALCHEMY_DATABASE_URI = r'mysql+pymysql://root:mysql@127.0.0.1:3306/mysql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base = declarative_base(engine)
    pass


class Config(BaseConfig):
    pass


config_dict = {
    "config": Config
}
