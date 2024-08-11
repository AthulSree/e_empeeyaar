from django.shortcuts import render #type: ignore
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect # type: ignore

from .models import*
from candidate.models import wallpostIPs

# Create your views here.

def docsquad_land(request):
    wp_ip = request.META.get('HTTP_X_REAL_IP','Anonym')
    context = {'option':'docsquad','my_ip':wp_ip}
    return render(request,'doc_squad.html',context)


def savefeedback(request):
    my_ip = request.POST.get('my_ip')
    feedback = request.POST.get('feedback')
    
    try:
        Feedback.objects.create(post_ip=my_ip, feedback=feedback)
        statuscode = 200
        msg = 'success'
    except Exception as e:
        msg = str(e)
        statuscode = 300
        
    return JsonResponse({'statuscode':statuscode,'msg':msg})


def displayOwnFolders(request):
     wp_ip = request.wp_ip
     uId = wallpostIPs.objects.get(ip = wp_ip)
     parentid = request.POST.get('parentid','None')
     if(parentid != 'None'):
        ownFolders = Docsquad.objects.filter(userId=uId,parent_id=parentid, disabled='N')
     else:
        ownFolders = Docsquad.objects.filter(userId=uId, disabled='N')
     context = {'folderlists':ownFolders, 'parentid':parentid}
     return render(request,'doc_squad_own_folder.html', context)

def saveNewFolder(request):
        wp_ip = request.META.get('HTTP_X_REAL_IP','Anonym')
        uId = wallpostIPs.objects.get(ip = wp_ip)
        folder_name = request.POST.get('docs_folderName')
        folder_privacy = request.POST.get('docs_folderprivacy')
        parent_id = None

        try:
            Docsquad.objects.create(userId=uId, file_type='D', name=folder_name, privacy=folder_privacy, parent_id=parent_id)
            status = 'success'
            msg = 'Successfully created'
        except Exception as e:
            msg = str(e)
            status = 'error'

        return JsonResponse({'status':status,'msg':msg})
        
def editFolder(request):
    fid = request.POST.get('fid')
    ddtype = request.POST.get('ddtype')
    newName = request.POST.get('newName','')

    try:
        if(ddtype == 'rename_folder'):
            folder = Docsquad.objects.get(id=fid)
            folder.name = newName
            folder.save()
            msg = 'Successfully renamed'
        if(ddtype == 'disable_folder'):
            folder = Docsquad.objects.get(id=fid)
            folder.disabled = 'Y'
            folder.save()
            msg = 'Successfully archived'
        if(ddtype == 'switch_privacy_folder'):
            folder = Docsquad.objects.get(id=fid)
            if(folder.privacy=='A'):
                folder.privacy = 'O'
            else:
                folder.privacy = 'A'
            folder.save()
            msg = 'Successfully switched'
        status = 'success'
    except Exception as e:
        status = 'error'
        msg = str(e)

    return JsonResponse({'status':status,'msg':msg})
