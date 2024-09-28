from django.urls import path
from . import views

urlpatterns = [
    path('', views.notiboiIndex, name='notiboi_index'),
    path('sendNotification/', views.sendNotification, name='send_notification')
]