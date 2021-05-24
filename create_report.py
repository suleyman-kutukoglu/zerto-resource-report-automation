import pandas as pd
from zerto_api_response import *
from mail import *
from report_date import *
from settings import get_logo_path, get_report_folder_path, get_file_name_format
from file_operations import create_folder_for_new_day
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Table, TableStyle


def get_vm_disk_usages_for_zorg(zorg_name):
    resource_json = get_resource_status(get_valid_report_day(), get_valid_report_day(), zorg_name)
    journal_total = float()
    volumes_total = float()
    vm_array = []
    for e in range(len(resource_json)):
        vm = list()
        vm.append(resource_json[e]["ProtectedSite"]["VmInfo"]["VmName"])
        vm.append("{:.2f}".format(
            float(resource_json[e]["RecoverySite"]["Storage"]["JournalProvisionedStorageInGB"])).replace('.', ','))
        vm.append("{:.2f}".format(
            float(resource_json[e]["RecoverySite"]["Storage"]["VolumesProvisionedStorageInGB"])).replace('.', ','))
        vm_array.append(vm)
        journal_total += float(resource_json[e]["RecoverySite"]["Storage"]["JournalProvisionedStorageInGB"])
        volumes_total += float(resource_json[e]["RecoverySite"]["Storage"]["VolumesProvisionedStorageInGB"])

    create_dataframe(zorg_name, vm_array, journal_total, volumes_total)


def create_dataframe(zorg_name, vm_array, journal_total, volumes_total):
    df = pd.DataFrame(vm_array, columns=['VM Name', 'Recovery Journal\nProvisioned Storage (GB)',
                                         'Recovery Volumes\nProvisioned Storage (GB)'])

    df.style.hide_index()
    data = [df.columns.to_list()] + df.values.tolist()
    table = Table(data, hAlign='RIGHT')
    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT')
    ]))
    table.hAlign = 'CENTER'

    create_story(table, zorg_name, journal_total, volumes_total)


def create_story(table, zorg_name, journal_total, volumes_total):
    paragraph_journal = Paragraph(
        "\n\nRecovery Journal Provisioned Storage: {:.2f} TB".format(journal_total / 1024).replace('.', ','),
        getSampleStyleSheet()["h2"])
    paragraph_volumes = Paragraph(
        "\n\nRecovery Volumes Provisioned Storage: {:.2f} TB".format(volumes_total / 1024).replace('.', ','),
        getSampleStyleSheet()["h2"])
    total = Paragraph("\n\nTotal: {:.2f} TB".format((volumes_total + journal_total) / 1024).replace('.', ','),
                      getSampleStyleSheet()["h2"])

    story = [Paragraph("ZORG: {}".format(zorg_name), getSampleStyleSheet()["Heading1"]),
             table, paragraph_journal, paragraph_volumes,
             total]

    create_pdf(story, zorg_name)


def draw_paragraph(canvas, msg, x, y, max_width, max_height):
    message_style = ParagraphStyle(getSampleStyleSheet()["h3"])
    message = msg.replace('\n', '<br />')
    message = Paragraph(message, style=message_style)
    w, h = message.wrap(max_width, max_height)
    message.drawOn(canvas, x, y - h)


def create_pdf(story, zorg_name):
    logo = get_logo_path()
    report_folder_path = get_report_folder_path()
    file_name = get_file_name_format()

    create_folder_for_new_day()

    c = Canvas(report_folder_path + "\\" + file_name.format(get_numeric_day_for_report(), get_month_name_for_report(),
                                                            get_year_for_report(), zorg_name))

    line_x_start = 230
    line_width = 150
    line_y = 440

    c.setStrokeColorCMYK(0.68, 0.44, 0, 0.41)
    c.setLineWidth(7)

    draw_paragraph(c, "Date: {:02d}.{:02d}.{}".format(int(get_numeric_day_for_report()),
                                                      int(get_numeric_month_for_report()), get_year_for_report()), 510,
                   835, 700, 25)
    c.drawImage(logo, line_x_start, line_y, width=line_width,
                preserveAspectRatio=True, mask='auto')
    f = Frame(inch, inch, 6 * inch, 9 * inch)
    f.addFromList(story, c)
    c.save()


def start_creating_report(mail):
    new_session()

    resource_json = get_resource_status(get_valid_report_day(), get_valid_report_day())
    zorgs = get_zorg_names(resource_json)
    print(get_valid_report_day())
    for zorg in zorgs:
        get_vm_disk_usages_for_zorg(zorg)
        print(f"Resource report created for {zorg}")

    end_session(header_for_resource_status())
    if mail:
        print()
        start_mail_operation()
