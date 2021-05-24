# Fill your ZVM informations
zvm_username = 'zvm-username'
zvm_password = 'zvm-password'
zvm_ip = 'zvm-ip'

# Fill your SMTP informations
smtp_server = 'smtp-server'
sender_mail = 'report@yourcompany.com'
smtp_username = 'your-smtp-username'
smtp_password = 'password'
smtp_port = 'smtp-port'


def get_zvm_username():
    return zvm_username


def get_zvm_password():
    return zvm_password


def get_zvm_ip():
    return zvm_ip


def get_smtp_server():
    return smtp_server


def get_sender_mail():
    return sender_mail


def get_smtp_username():
    return smtp_username


def get_smtp_password():
    return smtp_password


def get_smtp_port():
    return smtp_port
