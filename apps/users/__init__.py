from apps.blueprint_factory import BluePrintFactory

api_user = BluePrintFactory(key_word="user").generate_instance()

from .views import *
