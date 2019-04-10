from apps.frf.serializer import Serializer
from .models import User


class UserSerializer(Serializer):
    """
    用户序列化器
    """
    serializer_obj = User
    fields = ("User", "Host",)
