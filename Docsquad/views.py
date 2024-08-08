from django.shortcuts import render #type: ignore

# Create your views here.

def docsquad_land(request):
    return render(request,'doc_squad.html')