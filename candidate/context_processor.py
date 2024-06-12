from datetime import datetime
import calendar


def lastThreeMonths(request):
    today = datetime.today()
    month = today.month
    last_three_months = []

    for i in range(3):
        month_id = today.month-i
        month_name = calendar.month_name[month_id]
        last_three_months.append({'value':month_id, 'name':month_name})

    months_list = {1 : 'Jan',2:'Feb',3:'March',4:'April',5:'May',6:'June',7:'July',8:'Aug',9:'Sept',10:'Oct',11:'Nov',12:'Dec'}

    # ------- session hold
    request.session['cur_year_selected'] = 2024
    cur_month_selected = int(request.session.get('cur_month_selected',today.month))
    request.session['cur_month_selected'] = cur_month_selected

    current_month = months_list[cur_month_selected]

    return {'last_three_months':last_three_months, 'current_month':current_month, 'current_year':2024, 'cur_month_selected':cur_month_selected}
