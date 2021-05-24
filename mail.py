import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
from settings import get_report_folder_path, get_file_name_format, get_mail_list_path, get_mail_body_message, get_mail_subject
from report_date import get_numeric_day_for_report, get_month_name_for_report, get_year_for_report
from credentials import get_sender_mail, get_smtp_server, get_smtp_username, get_smtp_password, get_smtp_port

global mail_mode

SENDER_MAIL = get_sender_mail()


def send_mail(fromaddr, toaddr, ccaddr, zorg_name):
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddr)
    msg['Cc'] = ', '.join(ccaddr)
    msg['Subject'] = get_mail_subject()

    body = get_mail_body_message()

    msg.attach(MIMEText(body, 'plain', "utf-8"))

    report_folder_path = get_report_folder_path()
    filename_function_call = get_file_name_format()
    filename = filename_function_call.format(get_numeric_day_for_report(), get_month_name_for_report(), get_year_for_report(), zorg_name)

    attachment = open(report_folder_path + "\\" + filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP(get_smtp_server(), get_smtp_port())
    server.login(get_smtp_username(), get_smtp_password())
    text = msg.as_string()
    server.sendmail(fromaddr, (toaddr+ccaddr), text)
    server.quit()


def start_mail_operation():
    print('Mail operations started.')
    with open(get_mail_list_path(), 'r', encoding="utf-8") as f:
        zorgs_and_mails = json.load(f)

    for contact_name, contact_details in zorgs_and_mails["contacts"].items():
        to_mail = list(contact_details["mail"])
        cc = list(contact_details["cc"])

        send_mail(SENDER_MAIL, to_mail, cc, contact_name)
        print(f'The report mail was sent to {contact_name}')
