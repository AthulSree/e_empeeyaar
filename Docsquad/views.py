from django.shortcuts import render #type: ignore
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect # type: ignore

from .models import Feedback

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
        
    