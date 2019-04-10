import json
import os

from flask import Blueprint, jsonify, g, request, current_app, session


class BluePrintFactory(object):
    default_settings = {
        "name": "api_user",
        "import_name": __name__,
        "static_folder": "",
        "static_url_path": "",
        "template_folder": None,
        "url_prefix": None,
        "subdomain": None,
        "url_defaults": None,
        "root_path": None
    }

    def __init__(self, *args, **kwargs):
        # print(__file__)
        # print(os.path.dirname(os.path.abspath(__file__))+"/static/department")

        # os.path.dirname(os.path.abspath(self.__file__))+
        if "key_word" in kwargs:
            self.bp = Blueprint(name="api_" + kwargs["key_word"],
                                import_name=__name__, static_folder="./" + kwargs["key_word"] + "/static",
                                static_url_path=kwargs["key_word"] + "_static")
        else:
            self.bp = Blueprint(*args, **kwargs)
        self.bp.after_request(self.after_request)
        self.bp.before_request(self.before_request)
        # self.get_instance_path()

    @staticmethod
    def after_request(response):
        # 判断响应是否为json格式 排除静态文件
        content_type = response.headers.get("Content-Type")
        if content_type != "application/json":
            return response

        # 排除图片上传
        if request.path == "/files/ossfile":
            return response

        # 拦截解析响应数据
        data = json.loads(response.data.decode())

        # 尝试获取user
        try:
            user = g.user
        except Exception as e:
            user = None

        # 尝试获取admin
        try:
            admin = g.admin
        except Exception as e:
            admin = None

        # 如果都没有获取到则说明未登录
        if not user and admin is None:
            data["etc"] = "用户未登录"
            return jsonify(data)

        if user:
            data["etc"] = user.role.name
        if admin:
            data["etc"] = admin.user.role.name
        return jsonify(data)

    @staticmethod
    def before_request():
        print("=" * 100)
        print(request.path)
        print(request.method)
        print("=" * 100)

    def generate_instance(self):
        return self.bp
