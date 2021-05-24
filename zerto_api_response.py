import requests
import urllib3
from requests.auth import HTTPBasicAuth
from credentials import get_zvm_ip, get_zvm_username, get_zvm_password

user_name = get_zvm_username()
password = get_zvm_password()
zvm_ip = get_zvm_ip()
base_url = f"https://{zvm_ip}:9669/v1"
session = f"{base_url}/session/add"


def login(session_url, zvm_user, zvm_password):
    print('Getting ZVM API Token...')
    auth_info = "{\r\n\t\"AuthenticationMethod\":1\r\n}"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(session_url, headers=headers, data=auth_info, verify=False,
                             auth=HTTPBasicAuth(zvm_user, zvm_password))
    if response.ok:
        auth_token = response.headers['x-zerto-session']
        print("Api Token: " + auth_token)
        return auth_token
    else:
        print("HTTP %i - %s, Message %s" % (response.status_code, response.reason, response.text))


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
global zerto_session


def get_session():
    global zerto_session
    return zerto_session


def new_session():
    global zerto_session
    zerto_session = login(session, user_name, password)


def end_session(session_header):
    print('Session terminated.')
    requests.delete(base_url + '/session', headers=session_header, verify=False)


def header_for_resource_status():
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-zerto-session': get_session()
    }


def get_resource_status(start_time, end_time, zorg=''):
    resource_report_url = base_url + "/reports/resources?zorgName={}&startTime={}&endTime={}".format(zorg, start_time,
                                                                                                     end_time)

    headers = header_for_resource_status()

    resource_response = requests.get(resource_report_url, headers=headers, verify=False)
    if resource_response.ok:
        return resource_response.json()

    else:
        print("HTTP %i - %s, Message %s" % (
            resource_response.status_code, resource_response.reason, resource_response.text))


def get_zorg_names(resource_status):
    zorg_names = set()

    for e in range(len(resource_status)):
        zorg_names.add(resource_status[e]["Vpg"]["ZorgName"])

    return zorg_names


def show_zorg_names(start_time, end_time):
    new_session()
    api_response = get_resource_status(start_time, end_time)
    zorg_names = set()

    for e in range(len(api_response)):
        zorg_names.add(api_response[e]["Vpg"]["ZorgName"])
    print(15*"*")
    print(*list(zorg_names), sep='\n\n')
    print(15 * "*")
