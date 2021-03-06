from django.urls import path
from .views import action, addRecord, privacy, showRecords


urlpatterns=[
    path('command/', action, name="command_action" ),
    path('record/add/', addRecord, name="add_record"),
    path('record/show/', showRecords, name="show_records"),
    path("privacy-policy/", privacy)
]