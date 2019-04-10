from apps.frf.mixins import AllMethodMixin
from .serializers import UserSerializer
from apps.users import api_user


class UserViewSet(AllMethodMixin):
    serializer_class = UserSerializer



api_user.add_url_rule(r"users", view_func=UserViewSet.as_view("users"))
