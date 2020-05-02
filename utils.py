import datetime

def date_format(date_str, format='%H:%M'):
    dateObj = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    return dateObj.strftime(format)

def date_diff_hours(date_str, hours=2):
    dateObj = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    localDate = dateObj + datetime.timedelta(hours=2)
    return localDate.strftime('%Y-%m-%dT%H:%M:%S')