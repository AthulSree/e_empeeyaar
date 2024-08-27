from django.shortcuts import render #type: ignore
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect # type: ignore

from .models import*
from candidate.models import wallpostIPs
import logging

logging.basicConfig(level=logging.INFO)

# Create your views here.

def docsquad_land(request):
    wp_ip = request.wp_ip
    # getting distinct userids from a join django query
    uniq_ipnames = set()
    ipnames = Docsquad.objects.select_related('userId')
    for name in ipnames:
        uniq_ipnames.add((name.userId.id,name.userId.name))
                
    context = {'option':'docsquad','my_ip':wp_ip,'uniq_ipnames':uniq_ipnames}
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
     parentid = int(request.POST.get('parentid'))
     p_id = parentid
     if(parentid == 0):
        p_id = None

     ownFolders = Docsquad.objects.filter(userId=uId,parent_id=p_id, disabled='N')
    #  parentid = 0
     try:
        parent_chain = []
        while p_id is not None:
            folder_name = Docsquad.objects.get(id=p_id)
            parent_chain.insert(0,{'id':p_id,'name':folder_name.name , 'privacy':folder_name.privacy})
            parent = Docsquad.objects.values('parent_id').get(id=p_id)
            p_id = parent['parent_id']
     except Exception as e:
        logging.error(f"An error occurred: {e}")
     context = {'folderlists':ownFolders, 'parentid':parentid, 'parent_chain':parent_chain}
     return render(request,'doc_squad_own_folder.html', context)
 
 
def displayPublicFolders(request):
     uId = request.POST.get('u_id')
     parentid = int(request.POST.get('parentid'))
     p_id = parentid
     
     u_name = wallpostIPs.objects.get(id=uId)
     if(parentid == 0):
        p_id = None

     publicFolders = Docsquad.objects.filter(userId=uId,parent_id=p_id, disabled='N', privacy='A')
    #  parentid = 0
     try:
        parent_chain = []
        while p_id is not None:
            folder_name = Docsquad.objects.get(id=p_id)
            parent_chain.insert(0,{'id':p_id,'name':folder_name.name , 'privacy':folder_name.privacy})
            parent = Docsquad.objects.values('parent_id').get(id=p_id)
            p_id = parent['parent_id']
     except Exception as e:
        logging.error(f"An error occurred: {e}")
     context = {'folderlists':publicFolders, 'parentid':parentid, 'parent_chain':parent_chain,'user_name':u_name.name}
     return render(request,'doc_squad_public_folder.html', context)
 
 

def saveNewFolder(request):
        wp_ip = request.wp_ip
        uId = wallpostIPs.objects.get(ip = wp_ip)
        folder_name = request.POST.get('docs_folderName')
        folder_privacy = request.POST.get('docs_folderprivacy')
        parent_id = int(request.POST.get('parent_id'))
        if(parent_id == 0):
            parent_id = None
        else:
            parent_id = Docsquad.objects.get(id=parent_id)

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


def saveDragNDrop(request):
    wp_ip = request.wp_ip
    uId = wallpostIPs.objects.get(ip = wp_ip)
    if request.method == 'POST':
        if request.FILES:
            files = request.FILES.getlist('files[]')  # Retrieve list of files
            prentid_dir = request.POST.get('prentid_dir')
            doc_parent = Docsquad.objects.get(id=prentid_dir)

            for f in files:
                print(f)
                # Handle each file here
                try:
                    Docsquad.objects.create(userId=uId, file_type='F', name=f.name, privacy='A', parent_id=doc_parent, file_path=f)
                    status = 'success'
                    msg = 'Successfully created'
                except Exception as e:
                    msg = str(e)
                    status = 'error'
                    return JsonResponse({'status': 'error', 'msg': 'Some error occurred.'+msg})
                
            return JsonResponse({'status': 'success', 'msg': 'Files uploaded successfully.'})
        else:
            return JsonResponse({'status': 'error', 'msg': 'No files received.'})
    
    return JsonResponse({'status': 'error', 'msg': 'Invalid request method.'})
