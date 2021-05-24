import datetime


def get_now():
    return datetime.datetime.now()


def get_valid_report_day():
    return datetime.date.today() - datetime.timedelta(days=1)


def get_numeric_day():
    return datetime.date.today().day


def get_hour():
    return int(get_now().hour)


def get_minute():
    return int(get_now().minute)


def get_numeric_day_for_report():
    return get_valid_report_day().day


def get_numeric_month_for_report():
    return get_valid_report_day().month


def get_day_name_for_report():
    return get_valid_report_day().strftime("%A")


def get_month_name_for_report():
    return get_valid_report_day().strftime("%B")


def get_year_for_report():
    return get_valid_report_day().year
