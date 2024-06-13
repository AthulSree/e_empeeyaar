from django.shortcuts import render # type: ignore
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect # type: ignore
from django.template import loader # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.urls import reverse # type: ignore
from .models import Candidate,LeaveRecords
from datetime import datetime
from django.utils.dateparse import parse_date  # type: ignore
import pdfkit # type: ignore
from my_mpr.settings import WKHTMLTOPDF_PATH,MPR_HTML_HEAD,SIGNED_MPR_SIGN_IMG_PATH  # type: ignore



config = pdfkit.configuration(wkhtmltopdf = WKHTMLTOPDF_PATH)


def dashboard(request):
    context = {'option':'dashboard'}  # Add your context data here
    return render(request, 'dashboard.html', context)




def candidatelist(request):
    context = {'option':'candidatedetails'}
    return render(request, 'candidate_details.html', context)




def addcandidate(request):
    if(request.method=='POST'):
        print(request.POST)
        name = request.POST.get('cand_name')
        desig = request.POST.get('cand_desig')
        wonum = request.POST.get('cand_wonumber')
        proj_no = request.POST.get('cand_proj_num')
        join_date = request.POST.get('cand_join_date')
        # ------ Add candidate
        if(request.POST.get('cand_addmode')=='add'):
            try:
                candidate = Candidate.objects.create(name=name, designation=desig, joining_date=join_date, project_no=proj_no, workorder_no=wonum, entered_time=datetime.now())            
                return HttpResponseRedirect(reverse('add_candidate_success')+'?pagestat=200')
            except Exception as e:
                context = {'option':'candidatedetails','msg':str(e), 'pagestat':'500'}
                return render(request, 'candidate_details.html', context)
        # ------ Edit candidate
        elif(request.POST.get('cand_addmode')=='edit'):
             try:
                  c_id = request.POST.get('cand_id')
                  print(c_id)
                  candidate = Candidate.objects.get(c_id=c_id)
                  candidate.name=name
                  candidate.designation=desig
                  candidate.joining_date=join_date
                  candidate.project_no=proj_no
                  candidate.workorder_no=wonum
                  candidate.save()
                  return HttpResponseRedirect(reverse('add_candidate_success')+'?pagestat=204')
             except Exception as e:
                return HttpResponseRedirect(reverse('add_candidate_success')+'?pagestat=204')
    else:
        return render(request, 'candidate_details.html', {'pagestat':'500'})



def add_candidate_success(request):
            pagestat = request.GET.get('pagestat')
            context = {'option':'candidatedetails','pagestat':pagestat}
            return render(request, 'candidate_details.html', context)



def showallcandidates(request):
    #  query = "SELECT * FROM candidates"
    #  cands = Candidate.objects.raw(query)
     candidates = Candidate.objects.all().values
     context = {'candidatelist':candidates}
     return render(request,'allcandidateslist.html',context)
    #  print(candidates)



def leaveRecordList(request):
     context = {'option':'leave_records'}
     return render(request, 'candidate_leaves.html',context)



def leaveUpdatelist(request):
     month = request.session['cur_month_selected']
     year = request.session['cur_year_selected']
     query = " SELECT   C.c_id,C.name,L.month,L.year,L.paid_leave_days,L.non_paid_leave_days,L.no_of_leaves FROM candidates C LEFT JOIN leave_records L ON C.C_ID=L.C_ID AND L.MONTH = %s AND L.YEAR=%s "
     leaves = Candidate.objects.raw(query,[month,year])
     context = {'leave_records':leaves,'month_year':f"{month}/{year}"}
     return render(request,'leaveRecords_table.html',context)



def leaveRecordSave(request):
     s_month = request.session['cur_month_selected']
     s_year = request.session['cur_year_selected']
     if(request.method == 'POST'):
          req = request.POST
          cand_id = req.get('cand_id')
          paid_leaves = req.get('paidleaves')
          non_paid_leaves = req.get('non_paidleaves')

          delRecord = LeaveRecords.objects.filter(c_id=cand_id,month=6).delete()
          candidate = Candidate.objects.get(c_id=cand_id)
          paidleaveArr = paid_leaves.split(',')
          nonpaidleaveArr = non_paid_leaves.split(',')
          paidleaveArr = list(filter(lambda x: x.strip(), paidleaveArr))
          nonpaidleaveArr = list(filter(lambda x: x.strip(), nonpaidleaveArr))

          total_leaves = len(paidleaveArr)+len(nonpaidleaveArr)
          paid_leaves = ",".join(paidleaveArr)
          non_paid_leaves = ",".join(nonpaidleaveArr)
          addRecord = LeaveRecords.objects.create(
               year=s_year, 
               month=s_month, 
               paid_leave_days=paid_leaves, 
               non_paid_leave_days=non_paid_leaves, 
               c_id=candidate, 
               no_of_leaves=total_leaves)
          
          return JsonResponse({'msg':200})










def changeMonth(request):
     if(request.method == 'POST'):
          month = request.POST.get('month')
          request.session['cur_month_selected']=month
          return JsonResponse({'status':200})
     else:
          return JsonResponse({'status':500})


    
def gen_mpr(request):
    template = loader.get_template('mpr.html')
    return HttpResponse(template.render())



def generatepdf(request):
    absent_no = request.POST['age']
    mode = request.POST['mode']
    # pdf = pdfkit.from_url(request.build_absolute_uri(reverse('gen_mpr')),False, configuration=config)
    context = {'absent_no':absent_no,'from_date':'01/06/2024','html_header':MPR_HTML_HEAD, 'SIGNED_MPR_SIGN_IMG_PATH':SIGNED_MPR_SIGN_IMG_PATH}

    if(mode == '1'):
        html_content = render_to_string('mpr.html', context)
    elif(mode == '2'):
        html_content = render_to_string('mpr_with_sign.html',context) 

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access':"",
        'debug-javascript': None,
        'no-stop-slow-scripts': None,
        'log-level': 'info'
    }
    pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="file_name.pdf"'
    return response

