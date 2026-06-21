from django.urls import path
from . import views

urlpatterns = [
    path('', views.cup_start, name='cup_start'),
    path('select/', views.cup_select, name='cup_select'),
    path('ing/', views.cup_ing, name='cup_ing'),
    path('result/', views.cup_result, name='cup_result'),
    path('link/', views.cup_link, name='cup_link'),
    path('share/preview/', views.cup_share_preview, name='cup_share_preview'),
    path('result/preview/', views.cup_result_preview, name='cup_result_preview'),
    path('share/<str:share_token>/', views.cup_share, name='cup_share'),
    path('share/<str:share_token>/start/', views.cup_share_start, name='cup_share_start'),
]
