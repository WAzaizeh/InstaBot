import datetime as dt


def days_since_date(n):
    n = dt.datetime.strptime(n, '%d/%m/%Y').date()
    diff = dt.datetime.now().date() - n
    return diff.days
