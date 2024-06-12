from  django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('',views.dashboard, name="dashboard"),
    path('candidatedetails', views.candidatelist, name="candidate_details"),
    path('gen_mpr',views.gen_mpr, name="gen_mpr"),
    path('pdf',views.generatepdf, name="pdf"),
    path('addcandidates',views.addcandidate, name="add_candidates"),
    path('add_candidate_success',views.add_candidate_success, name="add_candidate_success"),
    path('showallcandidates', views.showallcandidates, name="showall_candidates"),
    path('leaveRecordList',views.leaveRecordList, name='leave_records'),
    path('leaveUpdatelist',views.leaveUpdatelist, name='leaveUpdate_list'),
    path('leaveRecordSave',views.leaveRecordSave, name='leaveRecord_Save')
]