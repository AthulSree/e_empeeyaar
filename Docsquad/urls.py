from  django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('',views.docsquad_land, name='docsquad_land'),
    path('display_OwnFolders/', views.displayOwnFolders, name='display_own_folders'),
    path('save_feedback/', views.savefeedback, name='savefeedback'),
    path('save_newfolder/',views.saveNewFolder, name='save_New_Folder' ),
    path('edit_Folder/',views.editFolder, name='edit_folder' )
]