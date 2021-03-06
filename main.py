import time
from settings import get_trigger_day, get_trigger_minute, get_trigger_hour, get_mail_mode
from create_report import *

# For debugging
from report_date import get_numeric_day, get_hour, get_minute

# Lists ZORG names at the specified date.
# show_zorg_names(get_valid_report_day(), get_valid_report_day())


def main():
    while True:
        day, hour, minute = get_numeric_day(), get_hour(), get_minute()

        print(f'Day: {day} Hour: {hour} Minute: {minute}')

        if get_numeric_day() == get_trigger_day() and get_hour() == get_trigger_hour() and get_minute() == get_trigger_minute():
            start_creating_report(get_mail_mode())
            time.sleep(120)

        if get_hour() == 8 and get_minute() == 0:
            start_creating_report(False)
            time.sleep(120)

        time.sleep(30)


main()
