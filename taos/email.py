from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from taos import config


def _get_email_string(**kwargs):
    return "<br>".join(
        [
            "<strong>New Contact Request</strong>",
            "New Contact request from taos-cli for {service_type}",
            "Requested by {name} at {email}.",
        ]
    ).format(**kwargs)


def send_message(name, email, service_type):
    message = Mail(
        from_email=email,
        to_emails=config.SUPPORT_EMAIL,
        subject=f"Contact Request from {name}",
        html_content=_get_email_string(
            name=name, email=email, service_type=service_type
        ),
    )

    try:
        sg = SendGridAPIClient(config.SEND_GRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

