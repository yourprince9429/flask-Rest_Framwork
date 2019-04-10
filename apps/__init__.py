import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from werkzeug.routing import BaseConverter
import redis
from config import config_dict
from flask_socketio import SocketIO
from raven.contrib.flask import Sentry

db = SQLAlchemy()

redis_cli = redis.StrictRedis(decode_responses=True)

socketio = SocketIO()


# sentry = Sentry(
#     dsn='http://8dff2e82b59f42cbac3435828cbba029:2b12a988b3ed4d068cc3aaffadbc641d@znsq.yuanjia101.com:9000/3')


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def set_log_level(log_level):
    # 设置日志的记录等级
    logging.basicConfig(level=log_level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log",
                                           maxBytes=1024 * 1024 * 100,
                                           backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter(
        '%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def CreateApp(configName):
    app = Flask(__name__)
    config_cls = config_dict[configName]
    app.config.from_object(config_cls)
    db.init_app(app)
    # 初始化socketio
    socketio.init_app(app)
    # 向app中添加自定义的路由转换器
    app.url_map.converters['re'] = RegexConverter
    # 设置日志追踪等级
    set_log_level(config_cls.LOG_LEVEL)

    # 创建session对象
    Session(app)

    # 创建mongo对象

    global redis_cli

    redis_cli = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT, decode_responses=True)
    # CSRFProtect(app)
    # 注册蓝图 url——prefix接收参数给url前缀
    from flask_cors import CORS  # flask做跨域处理
    CORS(app, supports_credentials=True)

    # todo 注册路由

    from apps import users
    app.register_blueprint(users.api_user, url_prefix='/users')

    # # Sentry监听
    # sentry.init_app(app)

    return app
