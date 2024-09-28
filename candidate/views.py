from django.shortcuts import render # type: ignore
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect # type: ignore
from django.template import loader # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.urls import reverse # type: ignore
from .models import Candidate,LeaveRecords,Wallpost,wallpostIPs,wallpostAccessRecords
from django.db.models import Q # type: ignore
from datetime import datetime,date
from django.utils.dateparse import parse_date  # type: ignore
import pdfkit,calendar,os,fitz,base64 # type: ignore
from django.utils import timezone #type: ignore
import pytz
# import time
# import pywhatkit as kit #type: ignore
from my_mpr.settings import WKHTMLTOPDF_PATH,MPR_HTML_HEAD,SIGNED_MPR_SIGN_IMG_PATH  # type: ignore
from django.core.mail import EmailMultiAlternatives # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
# from weasyprint import HTML # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore
import paramiko # type: ignore
import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)




config = pdfkit.configuration(wkhtmltopdf = WKHTMLTOPDF_PATH)


def dashboard(request):
    today = datetime.today()
    month = request.session.get('cur_month_selected',today.month)
    year = request.session.get('cur_year_selected',today.year)

    query = " SELECT   C.c_id,C.name,C.image,L.month,L.year,L.paid_leave_days,L.non_paid_leave_days,L.no_of_leaves,L.att_details,L.att_graph,L.id FROM candidates C LEFT JOIN leave_records L ON C.C_ID=L.C_ID AND L.MONTH = %s AND L.YEAR=%s  order by c_id"
    leaves = Candidate.objects.raw(query,[month,year])
    context = {'option':'dashboard','leave_records':leaves,'month_year':f"{month}/{year}"}
    print('MMMMM',leaves[0])
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
          
          leaveExists = LeaveRecords.objects.filter(c_id=cand_id,month=s_month,year=s_year)
          
          if(att_graph == None and leaveExists.exists()):
            att_graph_exist = LeaveRecords.objects.values('att_graph').get(c_id=cand_id,month=s_month,year=s_year)
            att_graph = att_graph_exist['att_graph']
          if(att_details == None and leaveExists.exists()):
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


def wallpost(request):
    my_ip = request.wp_ip    
    send_to = wallpostIPs.objects.all()       
    poststat = request.GET.get('poststat',200)
    
    # checking if the req ip is included in the universe
    try:
        user_id = wallpostIPs.objects.get(ip=my_ip)
    except ObjectDoesNotExist:
        return render(request,'notAMember.html')
    
    
    query = Wallpost.objects.filter(disabled = 'N')
    if(my_ip != '127.0.0.1'):
        query = query.filter((Q(send_to = '0')|Q(send_to = my_ip) | Q(posted_ip=my_ip)))
        query = query.filter()
    wallpost = query.order_by('-posted_time')

    try:
        wallpost_last_active = wallpostAccessRecords.objects.values('last_active_time').get(user=user_id)
        wallpost_last_active = wallpost_last_active['last_active_time']
    except wallpostAccessRecords.DoesNotExist:
        wallpost_last_active = datetime.strptime("Aug. 28, 2024, 10:56 PM", "%b. %d, %Y, %I:%M %p")
        wallpost_last_active = timezone.make_aware(wallpost_last_active, timezone=pytz.timezone('Asia/Kolkata')) 
          
    
     
    comparison_date = datetime(2024, 9, 4, 0, 0)
    comparison_date = timezone.make_aware(comparison_date, timezone=pytz.timezone('Asia/Kolkata'))
    
    context = {'option':'wall_post', 
               'wallpost':wallpost, 
               'send_to':send_to,
               'my_ip':my_ip,
               'poststat':poststat,
               'wallpost_last_active':wallpost_last_active,
               'comparison_date':comparison_date,
               'unReadAvail':0
               }
    return render(request, 'wall_post.html',context)





def wallpost_save(request):
    subject = request.POST.get("wp_subject")
    data = request.POST.get("wp_content")
    file = request.FILES.get("wp_img")
    wp_sendto_ip = request.POST.get("wp_sendto_ip")
    wp_ip = request.wp_ip
    wp_reply = int(request.POST.get('wp_reply_id'))
    
    # ----
    if(wp_sendto_ip == '10.162.6.11'):
        wp_sendto_ip = '127.0.0.1'
    # ----
    try:
        wp_by = wallpostIPs.objects.values('name').get(ip=wp_ip)['name']
    except ObjectDoesNotExist:
        wp_by = 'Anonym.'
     
    seen = 'N'
    if(wp_sendto_ip == '0'):
        seen = 'Y'

    wp_time = datetime.now()
    
    if(wp_reply > 0):
        wallpostContent = Wallpost.objects.get(id=wp_reply)
        wallpostContent.reply_content = data
        wallpostContent.reply_ip = wp_ip
        wallpostContent.reply_by = wp_by
        wallpostContent.reply_time = wp_time
        wallpostContent.save()
        # print('XXXXXXXXXXXXXXXXXXXXXXx',wallpostContent.posted_ip)
        if(wp_ip == wallpostContent.posted_ip):
            sendWallpostNoti(wp_by,wallpostContent.send_to,'reply')
        else:
            sendWallpostNoti(wp_by,wallpostContent.posted_ip,'reply')
            
            
    elif(data != "" or file != None):
        Wallpost.objects.create(subject=subject , content= data, files=file, posted_ip= wp_ip, posted_by= wp_by , send_to=wp_sendto_ip,seen=seen, posted_time=wp_time)
        sendWallpostNoti(wp_by,wp_sendto_ip,'new')
        

    return HttpResponseRedirect(reverse('wall_post')+'?poststat=200')


def sendWallpostNoti(sender,receiverId,mode):
    if(receiverId != 0):
        ipData = wallpostIPs.objects.filter(ip = receiverId).first()
        receiverIP = ipData.ip
        receiverPassword = ipData.password
        receiverUname = ipData.uname
        
        # ---noti
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(receiverIP, username=receiverUname, password=receiverPassword)
        if(mode =='new'):
            msg = f"{sender} has sent you a message in Byte-whaSSH!"
            
        else:
            msg = f"{sender} had replied to one of your message in Byte-whaSSH!"
        ssh.exec_command(f"notify-send -u critical -i /home/{receiverUname}/notification-bell.png  'New message in byte-WhaSSH`s WALLPOST' '{msg} \n\n\n Click to open Wallpost http://bytewash.com \n\n\n\t\t\t\t\t\t\t\t\t -Brahmoski' ")
        # -------
        
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('10.162.6.11', username="athul", password="nic*123")
    ssh.exec_command("notify-send 'New message in byte-WhaSSH'")
    

def wallpost_delete(request):
    postid = request.POST.get('postid')
    try:
        post = Wallpost.objects.get(id=postid)
        post.disabled = 'Y'
        post.save()      
        return JsonResponse({'status':200})
    except Exception as e:
        return JsonResponse({'status':300})


def wallpost_msg_read(request):
    wp_ip = request.wp_ip
    try:
        Wallpost.objects.filter(send_to=wp_ip).update(seen = 'Y')
        wp_user = wallpostIPs.objects.get(ip=wp_ip)

        try:
            wp_access = wallpostAccessRecords.objects.get(user = wp_user)
        except wallpostAccessRecords.DoesNotExist:
            wp_access = None

        if(wp_access):
            wp_access.last_active_time = datetime.now()
            wp_access.save()
        else:
            wallpostAccessRecords.objects.create(user=wp_user,last_active_time=datetime.now())
    except Exception as e:
        return JsonResponse({'status':300,'msg':str(e)})
        
    return JsonResponse({'status':200})


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
        file_name = name+"_mpr_"+str(s_month)+"_"+str(s_year)+".pdf"
    if(mode == 'lac'):
        html_content = render_to_string('lac.html', lac_context)
        file_name = name+"_lac_"+str(s_month)+"_"+str(s_year)+".pdf"
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
    # htmly = loader.get_template('email.html')
    # d = { 'username': name, 'month': s_mprformonth }
    # subject, from_email, to = 'E-empeeyar says hi!', 'athulsaas@gmail.com', 'nisanth7077@gmail.com'
    # html_content_email = htmly.render(d)
    # msg = EmailMultiAlternatives(subject, html_content_email, from_email, [to])
    # msg.attach_alternative(html_content_email, "text/html")
    # msg.send()
    ################################################################## 

    pdf = pdfkit.from_string(html_content, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+file_name
    return response
    #  run this command in a terminal to rename scanned files => python3 manage.py pdf2img

# ================== Other testing functions =========================>


def send_whatsapp_msgs(request):
    # pywhatkit.sendwhatmsg('+9170xxxxxxxx','*Thank for Choosing e-Empeeyar*<br>thanks')
    # for phone in phonenumbers:
    # kit.sendwhatmsg_instantly('+919539033379',"*Your MPR has been generated* \n Thanks for choosing e-Empeeyaar")
        # time.sleep(10)

    return JsonResponse({'status':400})




def process_pdfs(request):
    s_mprformonth = request.session['mprformonth']
    if request.method == 'POST':
        pdf_folder = 'D:\pdfs'
        target_names = ['ATHUL', 'SREERAJ','NISANTH','SIMI','ANUJITH','VIMAL']
        # renamed_files = []

        try:
            for filename in os.listdir(pdf_folder):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(pdf_folder, filename)
                    doc = fitz.open(file_path)
                    text = ''
                    for page in doc:
                        text += page.get_text()

                    new_name = find_name_in_text(text, target_names,s_mprformonth)
                    doc.close()
                    if new_name:
                        new_filename = f"{new_name}.pdf"
                        os.rename(file_path, os.path.join(pdf_folder, new_filename))
                        # renamed_files.append(new_filename)
            
            return JsonResponse({'status': 200})
        except Exception as e:
            return HttpResponse({'status': 300,'msg':str(e)})

    return HttpResponse({'status': 300,'msg':str(e)})

def find_name_in_text( text, names, s_mprformonth):
    for name in names:
        if name in text:
            if 'Monthly Performance Report' in text:
                return f"{name}_MPR_"+s_mprformonth
            elif 'Leave Adjustment Certificate' in text:
                return f"{name}_LAC_"+s_mprformonth
    return None





def open_remote_folder_view(request):
    transfer_and_open_folder()
    return HttpResponse("Remote folder has been opened locally.")

def transfer_and_open_folder():
    # Define the target host and connection details

    try:
        # Define the target host and connection details
        target_host = '10.162.6.12'  # Replace with the target system's IP address
        target_port = 22
        target_username = 'shershad'
        target_password = 'nic*123'
        remote_home_directory = '/home/shershad/'  # Replace with the remote folder path
        local_home_directory = '/home/athul/Documents'  # Replace with your local folder path

        # Create the local folder if it doesn't exist
        if not os.path.exists(local_home_directory):
            os.makedirs(local_home_directory)

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            target_host,
            username=target_username,
            password=target_password
        )

        # Start an SFTP session
        sftp = ssh.open_sftp()
        
        # Function to recursively download a directory
        def download_dir(remote_dir, local_dir):
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            for item in sftp.listdir(remote_dir):
                remote_item = os.path.join(remote_dir, item)
                local_item = os.path.join(local_dir, item)
                try:
                    # Check if the remote item is a file or directory
                    if sftp.stat(remote_item).st_mode & 0o40000:  # Directory
                        download_dir(remote_item, local_item)
                    else:  # File
                        sftp.get(remote_item, local_item)
                except IOError as e:
                    logging.error(f"Error accessing {remote_item}: {e}")
        
        # Download the home directory
        download_dir(remote_home_directory, local_home_directory)

        # Close the SFTP session and SSH connection
        sftp.close()
        ssh.close()

        # Open the local folder
        if os.name == 'nt':  # Windows
            os.startfile(local_home_directory)
        elif os.name == 'posix':  # macOS or Linux
            subprocess.run(['open', local_home_directory] if sys.platform == 'darwin' else ['xdg-open', local_home_directory])

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise  # Re-raise the exception for further debugging
    
    
    
# my_app/views.py

# my_app/views.py

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .utils.sftp_client import SFTPClient
import zipfile
import os
import io
import stat

def connect_to_server(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        port = int(request.POST.get('port', 22))
        username = request.POST.get('username')
        password = request.POST.get('password')

        request.session['hostname'] = hostname
        request.session['port'] = port
        request.session['username'] = username
        request.session['password'] = password

        return redirect('list_dir', path='/')

    return render(request, 'connect2server.html', {'option':'uconnect'})

def list_dir(request, path):
    hostname = request.session.get('hostname')
    port = request.session.get('port')
    username = request.session.get('username')
    password = request.session.get('password')

    if not all([hostname, port, username, password]):
        messages.error(request, 'Missing connection information. Please reconnect.')
        return redirect('connect_to_server')

    sftp_client = SFTPClient(hostname, port, username, password)
    sftp_client.connect()

    try:
        file_attrs = sftp_client.list_dir(path)
    except Exception as e:
        messages.error(request, f'Error listing directory: {e}')
        return redirect('connect_to_server')
    finally:
        sftp_client.disconnect()

    file_list = [
        {'name': f.filename, 'is_dir': stat.S_ISDIR(f.st_mode)}
        for f in file_attrs
        if not f.filename.startswith('.')
    ]

    return render(request, 'list_dir.html', {'file_list': file_list, 'current_path': path})

def download_file(request, path):
    hostname = request.session.get('hostname')
    port = request.session.get('port')
    username = request.session.get('username')
    password = request.session.get('password')

    if not all([hostname, port, username, password]):
        messages.error(request, 'Missing connection information. Please reconnect.')
        return redirect('connect_to_server')

    sftp_client = SFTPClient(hostname, port, username, password)
    sftp_client.connect()

    local_path = os.path.join('/tmp', os.path.basename(path))

    try:
        sftp_client.get_file(path, local_path)
        with open(local_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(path)}'
            return response
    except Exception as e:
        messages.error(request, f'Error downloading file: {e}')
        return redirect('list_dir', path=os.path.dirname(path))
    finally:
        sftp_client.disconnect()
        if os.path.exists(local_path):
            os.remove(local_path)

def download_directory(request, path):
    hostname = request.session.get('hostname')
    port = request.session.get('port')
    username = request.session.get('username')
    password = request.session.get('password')

    if not all([hostname, port, username, password]):
        messages.error(request, 'Missing connection information. Please reconnect.')
        return redirect('connect_to_server')

    sftp_client = SFTPClient(hostname, port, username, password)
    sftp_client.connect()

    try:
        zip_buffer = sftp_client.compress_dir(path)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(path)}.zip'
        return response
    except Exception as e:
        messages.error(request, f'Error compressing and downloading directory: {e}')
        return redirect('list_dir', path=os.path.dirname(path))
    finally:
        sftp_client.disconnect()
