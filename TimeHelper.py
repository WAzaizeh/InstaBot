import datetime as dt


def days_since_date(n):
    n = dt.datetime.strptime(n, '%Y-%m-%d').date()
    diff = dt.datetime.now().date() - n
    return diff.days

def minutes_since(start):
    end = dt.datetime.now()
    elapsed = end - start
    return elapsed.total_seconds() / 60.0
