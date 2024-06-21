from django.shortcuts import render # type: ignore
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect # type: ignore
from django.template import loader # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.urls import reverse # type: ignore
from .models import Candidate,LeaveRecords
from datetime import datetime,date
from django.utils.dateparse import parse_date  # type: ignore
import pdfkit # type: ignore
import calendar
import time
import pywhatkit as kit #type: ignore
from my_mpr.settings import WKHTMLTOPDF_PATH,MPR_HTML_HEAD,SIGNED_MPR_SIGN_IMG_PATH  # type: ignore
from django.core.mail import EmailMultiAlternatives # type: ignore
from django.template.loader import get_template




config = pdfkit.configuration(wkhtmltopdf = WKHTMLTOPDF_PATH)


def dashboard(request):
    today = datetime.today()
    month = request.session.get('cur_month_selected',today.month)
    year = request.session.get('cur_year_selected',today.year)
    request.session['cur_month_selected'] = month #setting session for month
    request.session['cur_year_selected'] = year #setting session for year

    query = " SELECT   C.c_id,C.name,C.image,L.month,L.year,L.paid_leave_days,L.non_paid_leave_days,L.no_of_leaves,L.att_details,L.att_graph,L.id FROM candidates C LEFT JOIN leave_records L ON C.C_ID=L.C_ID AND L.MONTH = %s AND L.YEAR=%s  order by c_id"
    leaves = Candidate.objects.raw(query,[month,year])
    context = {'option':'dashboard','leave_records':leaves,'month_year':f"{month}/{year}"}

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
        profile_pic = request.FILES.get('profile_pic')
        print(profile_pic)
        gender = request.POST.get('cand_gender')
        # ------ Add candidate
        if(request.POST.get('cand_addmode')=='add'):
            try:
                candidate = Candidate.objects.create(name=name, designation=desig, joining_date=join_date, project_no=proj_no, workorder_no=wonum, entered_time=datetime.now(), image=profile_pic, gender=gender)            
                return HttpResponseRedirect(reverse('add_candidate_success')+'?pagestat=200')
            except Exception as e:
                context = {'option':'candidatedetails','msg':str(e), 'pagestat':'500'}
                return render(request, 'candidate_details.html', context)
        # ------ Edit candidate
        elif(request.POST.get('cand_addmode')=='edit'):
             try:
                  c_id = request.POST.get('cand_id')
                  candidate = Candidate.objects.get(c_id=c_id)
                  candidate.name=name
                  candidate.designation=desig
                  candidate.joining_date=join_date
                  candidate.project_no=proj_no
                  candidate.workorder_no=wonum
                  if(profile_pic != None):
                    candidate.image=profile_pic
                  candidate.gender=gender
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
     candidates = Candidate.objects.all()
     context = {'candidatelist':candidates}
     return render(request,'allcandidateslist.html',context)
    #  print(candidates)



def leaveRecordList(request):
     context = {'option':'leave_records'}
     return render(request, 'candidate_leaves.html',context)



def leaveUpdatelist(request):
     month = request.session['cur_month_selected']
     year = request.session['cur_year_selected']
     query = " SELECT   C.c_id,L.id,C.name,C.image,L.month,L.year,L.paid_leave_days,L.non_paid_leave_days,L.no_of_leaves,L.att_details,L.att_graph FROM candidates C LEFT JOIN leave_records L ON C.C_ID=L.C_ID AND L.MONTH = %s AND L.YEAR=%s order by c_id"
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
          att_graph = request.FILES.get('att_graph')
          att_details = request.FILES.get('att_details')
          
          if(att_graph == None):
            att_graph_exist = LeaveRecords.objects.values('att_graph').get(c_id=cand_id,month=s_month,year=s_year)
            att_graph = att_graph_exist['att_graph']
          if(att_details == None):
            att_details_exist = LeaveRecords.objects.values('att_details').get(c_id=cand_id,month=s_month,year=s_year)
            att_details = att_details_exist['att_details']

          LeaveRecords.objects.filter(c_id=cand_id,month=s_month,year=s_year).delete()

          candidate = Candidate.objects.get(c_id=cand_id)
          paidleaveArr = paid_leaves.split(',')
          nonpaidleaveArr = non_paid_leaves.split(',')
          paidleaveArr = list(filter(lambda x: x.strip(), paidleaveArr))
          nonpaidleaveArr = list(filter(lambda x: x.strip(), nonpaidleaveArr))

          total_leaves = len(paidleaveArr)+len(nonpaidleaveArr)
          paid_leaves = ",".join(paidleaveArr)
          non_paid_leaves = ",".join(nonpaidleaveArr)
   
          LeaveRecords.objects.create(
            year=s_year, 
            month=s_month, 
            paid_leave_days=paid_leaves, 
            non_paid_leave_days=non_paid_leaves, 
            c_id=candidate, 
            no_of_leaves=total_leaves,
            att_graph=att_graph,
            att_details=att_details
            )
          
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
    cand_id = request.POST['cand_id']
    mode = request.POST['mode']
    s_month = request.session['cur_month_selected']
    s_year = request.session['cur_year_selected']
    s_mprformonth = request.session['mprformonth']
    today = date.today()


    candidateDetails = Candidate.objects.get(c_id = cand_id)
    name = candidateDetails.name
    designation = candidateDetails.designation
    project_no = candidateDetails.project_no
    workorder_no = candidateDetails.workorder_no
    gender = candidateDetails.gender
    joining_date = candidateDetails.joining_date
    joining_date_f = joining_date.strftime('%d/%m/%Y')

    from_date = date(today.year,today.month,1)
    from_date_f = from_date.strftime('%d/%m/%Y')
    to_date = date(today.year,today.month,calendar.monthrange(today.year,today.month)[1])
    to_date_f = to_date.strftime('%d/%m/%Y')


    leavedetails = LeaveRecords.objects.get(c_id = cand_id, month = s_month, year = s_year)
    leaves = leavedetails.no_of_leaves
    leave_days = leavedetails.paid_leave_days
    leave_list = ''


    if(leaves > 0):
        if((leavedetails.non_paid_leave_days) != ""):
            leave_days = leave_days +","+leavedetails.non_paid_leave_days

        leave_arr = leave_days.split(',')
        leaveFormat = []

        for days in leave_arr :
            leaveFormat.append(datetime.strptime(f"{days}/{s_month}/{s_year}","%d/%m/%Y").strftime("%d/%m/%Y"))

        if len(leaveFormat) > 1:
            leave_list = ", ".join(leaveFormat[:-1]) + " and " + leaveFormat[-1]
        else:
            leave_list = leaveFormat[0]



    mpr_context = {'proj_no': project_no, 'mpr_for_month': s_mprformonth, 'wo_no': workorder_no, 'name': name, 'designation': designation, 'doj':joining_date_f, 'from_date':from_date_f, 'to_date':to_date_f, 'leave_no': leaves, 'html_header':MPR_HTML_HEAD,'SIGNED_MPR_SIGN_IMG_PATH':SIGNED_MPR_SIGN_IMG_PATH}


    lac_context = {'project_no': project_no, 'work_order_no': workorder_no, 'cand_name': name, 'gender':gender, 'leave_no': leaves, 'leave_list': leave_list, 'html_header':MPR_HTML_HEAD }

    if(mode == 'mpr'):
        html_content = render_to_string('mpr.html', mpr_context)
    if(mode == 'lac'):
        html_content = render_to_string('lac.html', lac_context)
    elif(mode == '2'):
        html_content = render_to_string('mpr_with_sign.html',mpr_context) 

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
    ######################### mail system #################################### 
    htmly = get_template('email.html')
    d = { 'username': name, 'month': s_mprformonth }
    subject, from_email, to = 'E-empeeyar says hi!', 'athulsaas@gmail.com', 'nisanth7077@gmail.com'
    html_content_email = htmly.render(d)
    msg = EmailMultiAlternatives(subject, html_content_email, from_email, [to])
    msg.attach_alternative(html_content_email, "text/html")
    msg.send()
    ################################################################## 

    pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="file_name.pdf"'
    return response


def send_whatsapp_msgs(request):
    # pywhatkit.sendwhatmsg('+9170xxxxxxxx','*Thank for Choosing e-Empeeyar*<br>thanks')
    # for phone in phonenumbers:
    kit.sendwhatmsg_instantly('+919539033379',"*Your MPR has been generated* \n Thanks for choosing e-Empeeyaar")
        # time.sleep(10)

    return JsonResponse({'status':400})