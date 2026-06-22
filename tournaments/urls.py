from django.urls import path
from .views import *

app_name = "tournaments"

urlpatterns = [
    path("", tournament_main, name="main"),
    path("create/", tournament_create, name="create"),
    path("<int:pk>/play/", tournament_play, name="play"),
    path("<int:pk>/result/", tournament_result, name="result"),
    path("<int:pk>/share/", generate_share_link, name="create_share"),
    path("<int:pk>/restart/", tournament_restart, name="restart"),
    path("share/<uuid:token>/", shared_play, name="shared_play"),
    path("record/", tournament_record, name="record"),  ## url 연결 'tournaments:record'로 하시면 됩니다
]