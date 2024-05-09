import datetime


class DateUtility:

    def format_time(access_time: datetime.date):
        try:
            return access_time.strftime('%H:%M')
        except ValueError:
            return access_time 

    def format_date(access_time: datetime.date):
        try:
            return access_time.strftime('%d-%m-%Y')
        except ValueError:
            return access_time 