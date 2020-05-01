import datetime

def format_date(date_str, format='%H:%M'):
    dateObj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    localDate = dateObj + datetime.timedelta(hours=2)
    return localDate.strftime(format)