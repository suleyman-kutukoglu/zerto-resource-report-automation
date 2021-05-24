from report_date import *

TRIGGER_DAY = 10
TRIGGER_HOUR =10
TRIGGER_MINUTE = 0

MAIL_MODE = True

logo_path = 'Your Logo path'
mail_json_path = 'Your mail.json file path'
reports_folder = 'Your reports folder path'


def get_mail_mode():
    return MAIL_MODE


def get_trigger_day():
    return TRIGGER_DAY


def get_trigger_hour():
    return TRIGGER_HOUR


def get_trigger_minute():
    return TRIGGER_MINUTE


def get_report_folder_path():
    return reports_folder + "{}.{:02d}.{}".format(get_numeric_day_for_report(), get_numeric_month_for_report(),
                                                  get_year_for_report())


def get_file_name_format():
    return 'Zerto_VmsResourcesReport_{}_{}_{}_{}.pdf'


def get_logo_path():
    return logo_path


def get_mail_list_path():
    return mail_json_path


def get_mail_subject():
    return 'Zerto Usage Report'


def get_mail_body_message():
    return 'Hello,\n\nThis is your disk usage report.'
