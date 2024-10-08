from  django.urls import path # type: ignore
from . import views

from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore



urlpatterns = [
    path('dashboard',views.dashboard, name="dashboard"),
    path('candidatedetails', views.candidatelist, name="candidate_details"),
    path('gen_mpr',views.gen_mpr, name="gen_mpr"),
    path('pdf',views.generatepdf, name="pdf"),
    path('addcandidates',views.addcandidate, name="add_candidates"),
    path('add_candidate_success',views.add_candidate_success, name="add_candidate_success"),
    path('showallcandidates', views.showallcandidates, name="showall_candidates"),
    path('leaveRecordList',views.leaveRecordList, name='leave_records'),
    path('leaveUpdatelist',views.leaveUpdatelist, name='leaveUpdate_list'),
    path('leaveRecordSave',views.leaveRecordSave, name='leaveRecord_Save'),
    path('changeMonth',views.changeMonth, name='change_month'),
    path('send_whatsapp_msgs',views.send_whatsapp_msgs, name='send_whatsapp_message'),
    path('',views.wallpost, name="wall_post"),
    path('wall_post_save',views.wallpost_save, name='wall_post_save'),
    path('process_pdfs', views.process_pdfs, name='process_pdfs'),
    path('wall_post_delete',views.wallpost_delete, name="wall_post_delete"),
    # path('apitest',views.apitest,name='apitest'),
    path('open-remote-folder', views.open_remote_folder_view, name='open_remote_folder_view'),
    
    path('connect/', views.connect_to_server, name='connect_to_server'),
    path('list_dir/<path:path>/', views.list_dir, name='list_dir'),
    path('download/<path:path>/', views.download_file, name='download_file'),
    path('download_directory/<path:path>/', views.download_directory, name='download_directory'),
    path('wallpostMsgRead', views.wallpost_msg_read, name='wallpost_msg_read'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
