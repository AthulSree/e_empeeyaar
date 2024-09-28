from django.shortcuts import render
from django.http import JsonResponse
import paramiko

# Create your views here.


def notiboiIndex(request):
    print('asdasdcasascdas')
    context =  {'option':'notiboi'}
    return render(request,'notiboi/notiboi.html',context)

def sendNotification(request):
    ip = request.POST.get('hostname')
    uname = request.POST.get('username')
    password = request.POST.get('password')
    content = request.POST.get('content')
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh.connect(ip,username=uname,password=password)
    
    ssh.exec_command(f"notify-send -u normal -i dialog-warning 'Hey Old maan....' '\n{content}' ")
    return JsonResponse({'status':'success','msg':'Notification sent successfully'})
    
    