import re


def date_handler(func):
    def formatter(request, delivery_date=None, order_date=None):
        date = order_date if delivery_date is None else delivery_date
        year_month_date = re.split("-", date)

        def validator(request, year_month_date):
            if len(year_month_date) != 3:
                raise ValueError('Wrong date format')
            return func(request, year_month_date)
        return validator(request, year_month_date)
    return formatter
