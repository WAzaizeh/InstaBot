import datetime as dt


def days_since_date(n):
    n = dt.datetime.strptime(n, '%d/%m/%Y').date()
    diff = dt.datetime.now().date() - n
    return diff.days

def minutes_since_start(start):
    end = dt.datetime.now()
    elapsed = end - start
    return elapsed.total_seconds() / 60.0
