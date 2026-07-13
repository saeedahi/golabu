from jalali_date import date2jalali

def to_shamsi(date):
    date = date2jalali(date).strftime('%Y-%M-%d')
    date = date.replace('/', '-')
    return date