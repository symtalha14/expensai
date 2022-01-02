from django.urls import path
from .views import action


urlpatterns=[
    path('command/', action, name="command_action" )
]