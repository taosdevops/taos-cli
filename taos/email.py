from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from taos import config


def _get_email_string(message_type="contact", **kwargs):
    _email_string_types = {
        "contact":"<br>".join([
            "<strong>New Contact Request</strong>",
            "New Contact request from taos-cli for {service_type}",
            "Requested by {name} at {email}."
        ]),
        "subscribe":"<br>".join([
            "<strong>New Contact Request</strong>",
            "New Contact request from taos-cli for {service_type}",
            "Requested by {name} at {email}.",
            ("For hours: {hours} , length of contract: {length},"
             " preferred communication: {communication}")
        ])
    }
    try:
        return _email_string_types[message_type].format(**kwargs)
    except KeyError: return ""


def send_message(email, name, message_type="contact", **kwargs):
    if "mailto" in email:
        email = email.split(':')[1].split('|')[0]
    print(kwargs)
    message = Mail(
        from_email=email,
        to_emails=config.SUPPORT_EMAIL,
        subject=f"Contact Request from {name}",
        html_content=_get_email_string(
            email=email, name=name, message_type=message_type ,**kwargs
        ),
    )

    try:
        sg = SendGridAPIClient(config.SEND_GRID_API_KEY)
        response = sg.send(message)
        return response
    except Exception as e:
        print(str(e))
