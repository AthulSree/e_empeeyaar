from django import template # type: ignore
from datetime import datetime
from ..models import LeaveRecords #type: ignore
from my_mpr.settings import MEDIA_URL


register = template.Library()

@register.filter
def format_leave_days(days,month_year):
    if(days == None):
        return None
    
    month,year=month_year.split('/')
    formatted_days = []
    for day in days.split(','):
        try:
            formatted_day = datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y").strftime("%d/%m/%Y")
            formatted_days.append(formatted_day)
        except ValueError:
            continue

    return formatted_days


@register.filter
def getatt1url(id):
    att1url_meta = LeaveRecords.objects.values('att_graph').get(id=id)
    att1url = MEDIA_URL+att1url_meta['att_graph']
    print(att1url)
    return att1url

@register.filter
def getatt2url(id):
    att1url_meta = LeaveRecords.objects.values('att_details').get(id=id)
    att1url = MEDIA_URL+att1url_meta['att_details']
    print(att1url)
    return att1url


