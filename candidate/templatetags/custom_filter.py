from django import template # type: ignore
from datetime import datetime


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
