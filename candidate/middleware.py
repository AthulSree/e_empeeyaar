from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
from datetime import datetime

class CheckSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Debugging: Check if session is initialized
        if request.session is None:
            print("Request session is None!")
        else:
            print(f"Request session initialized: {request.session}")

        today = datetime.today()
        month = request.session.get('cur_month_selected', today.month)
        year = request.session.get('cur_year_selected', today.year)
        
        
        request.session['cur_month_selected'] = month  # Setting session for month
        request.session['cur_year_selected'] = year
      

        response = self.get_response(request)
        return response

