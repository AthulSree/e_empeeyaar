from django import template # type: ignore
from datetime import datetime
from ..models import LeaveRecords #type: ignore
from my_mpr.settings import MEDIA_URL
from django.utils.html import escape, mark_safe #type: ignore
import re,os


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

@register.filter(name='style_contents')
def style_contents(value):
    """
    Replace text surrounded by ** with HTML bold tags, while escaping other HTML.
    """
    escaped_value = escape(value)
    bolded_value = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', escaped_value)
    italics_value = re.sub(r'\_\_(.*?)\_\_', r'<i>\1</i>', bolded_value)
    return mark_safe(italics_value)

@register.filter(name='is_pdf')
def is_pdf(file_url):
    return os.path.splitext(file_url)[1].lower() == '.pdf'

@register.filter(name='is_zip')
def is_zip(file_url):
    return os.path.splitext(file_url)[1].lower() == '.zip'


@register.filter(name='getFileName')
def get_FileName(filename):
    return filename.rstrip('/').split('/')[-1]




@register.filter(name='test_filter')
def test_filter(value):
    print("Custom filter applied!")
    return f"Test filter applied: {value}"