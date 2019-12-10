from taos.email import send_message

def send_message(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    try:
        name = request_json["name"]
        email = request_json["email"]
        service_type = request_json["service_type"]
        return send_message(name, email, service_type)


def cloud_function(request, *args, **kwargs):
    return send_message(request)
