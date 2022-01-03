from django.urls import path
from .views import action, addRecord, showRecords


urlpatterns=[
    path('command/', action, name="command_action" ),
    path('record/add/', addRecord, name="add_record"),
    path('record/show/', showRecords, name="show_records")
]