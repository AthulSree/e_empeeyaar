from  django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('',views.docsquad_land, name='docsquad_land'),
    path('save_feedback', views.savefeedback, name='savefeedback')
]