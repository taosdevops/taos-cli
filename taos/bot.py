import os
import slack
from pprint import pprint
from taos import bio, about, email
import traceback

slack_token = os.environ["SLACK_API_TOKEN"]
bot_data = slack.WebClient(token=slack_token).auth_test()
bot_string = f"<@{bot_data['user_id']}>"

bio_users = bio.list_persons()
about_services =[
    service['name'] for service in about.list_services()
    if service.get('name') and service['name'] != ''
]

partial_commands = {}
print("BOT Running")
print("BOT Info", bot_data)


def _is_thread_reply(payload: dict)-> bool:
    return "thread_ts" in payload.get("data", {})

def _has_parameter(command_string: dict, param_prefix="--")-> bool:
    return param_prefix in command_string

def _parse_command_string(command_string: str):
    pass
    if _has_parameter(command_string):
        command_string, *params = [
            part.strip() for part in command_string.split("--")
        ]
        parameter = {
            key :" ".join(values)
            for param_string in params
            for key, *values in [param_string.split(' ')]
        }
    else:
        parameter = {}
    return command_string, parameter

def _get_thread(payload: dict)-> str:
    data = payload.get("data", {})
    return data.get("thread_ts") or data.get("ts")

def _is_bot(data, **kwargs):
    return "bot_id" in data and data["bot_id"] == bot_data["bot_id"]

# Decorators
def talking_to_me(func):
    def _internal_(**payload):
        data = payload["data"]
        if not bot_string in data.get("text", []):
            return
        return func(**payload)

    return _internal_


def continue_partial(func):
    def _internal_(*args, **payload):
        if _is_bot(**payload) or not _is_thread_reply(payload):
            return

        try:
            thread_id = _get_thread(payload)
            command = partial_commands[thread_id]
        except KeyError:
            return

        pprint({"ContinuePayload": payload})
        return func(**payload, **command)

    return _internal_


def respond_to_slack(func):
    def _internal_(*args, web_client=None, **kwargs):
        try:
            pprint(kwargs)
            response = func(*args, **kwargs)

            if not isinstance(response, list):
                response = [response] if response else []

            data = kwargs.get("data", {})
            channel_id = data.get("channel")
            thread_ts = data.get("ts")

            for message in response:
                try:
                    message = message.decode()
                except AttributeError:
                    pass

                web_client.chat_postMessage(
                    channel=channel_id, text=message, thread_ts=thread_ts
                )
            return response
        except Exception as e:
            print(f"HIT Exception RESPOND:{e}")
            print(traceback.format_exc())

    return _internal_

def fetch_partial(func):
    def _internal_(*args, **payload):
        try:
            if payload:
                partial_command = partial_commands[_get_thread(payload)]
                return func(*args, partial=partial_command, **payload)
        except KeyError: pass
        return func(*args, payload=payload, **payload)
    return _internal_

# End Decorators

@slack.RTMClient.run_on(event="message")
@talking_to_me
def processor(**payload):
    data = payload["data"]
    raw_command_text = data.get("text", "").strip()
    commands = [ # Check all registered commands against text
        command
        for command, response in botcommands.items()
        if f"{bot_string} {command}" in raw_command_text
    ]

    if len(commands) > 0:
        # try:
        #     raw_command_string = raw_command_text.split(bot_string)[1]
        try:
            raw_command_string = raw_command_text.split(bot_string)[1].strip()
            # command_string = raw_command_text.split(bot_string)[1].strip()
            command_string, parameters = _parse_command_string(raw_command_string)
            botcommands[commands[0]](
                *command_string.split(" "),parameters=parameters, **payload
            )
        except Exception as e:
            print(e)

    else:
        web_client = payload["web_client"]
        channel_id = data["channel"]
        thread_ts = data["ts"]
        web_client.chat_postMessage(
            channel=channel_id, text=f"Where you talking to me?", thread_ts=thread_ts
        )
    return "ERROR"


@slack.RTMClient.run_on(event="message")
@continue_partial
def continuer(command_name, data, **payload):
    if _is_bot(data): print("BOT DETECTED") # For Debugging
    raw_command_text = data.get("text", "").strip()
    try:
        raw_command_string = raw_command_text.split(bot_string)[1]
        # command_string = data.get("text", "").split(bot_string)[1].strip()
        command_string, parameters = _parse_command_string(raw_command_string)
    except IndexError:
        command_string, parameters = _parse_command_string(raw_command_text)

    botcommands[command_name](
        command_name, *command_string.split(" "),
        data=data, parameters=parameters, **payload
    )


@respond_to_slack
def _parse_about(command_name, *args, **payload):
    newline_join = lambda items: "\n".join(items)
    if len(args) < 1:

        partial_commands[_get_thread(payload)] = {"command_name": "about"}
        print("Partial", partial_commands)
        return newline_join([
            "Thanks for asking about me.",
            *about.get_about()
        ])
        return f"What do you want to know about?"

    services_found = [service for service in args if service in about_services]
    if len(services_found) < 1:
        return "\n".join(
            [
                f"Sorry I dont know anything about {' '.join(args)}.",
                "These are the services that I do know about.",
                *[f"- {service}" for service in about_services],
            ]
        )

    return [
        newline_join(about.get_service(service))
        for service in services_found
    ]

@respond_to_slack
def _parse_bio(command_name, *args, **payload):
    if len(args) < 1:
        print(_get_thread(payload))
        partial_commands[_get_thread(payload)] = {"command_name": "bio"}
        print("Partial", partial_commands)
        return "Whos bio would you like to see?"

    bios_found = [user for user in args if user in bio_users]
    if len(bios_found) < 1:
        return "\n".join(
            [
                "Sorry we couldnt find the users that you posted.",
                "These are the bios that I could locate.",
                *[f"- {bio_user}" for bio_user in bio_users],
            ]
        )
    return [bio.get_user(user) for user in bios_found]

@respond_to_slack
@fetch_partial
def _parse_contact(command_name, *args, parameters=None, partial=None, **payload):
    # print("Partial",partial)
    # print("Args", args)
    # print("Parameters", parameters)
    params = {
        "email": "Email Address",
        "name": "Person to contact",
        "service-type": "What services are you looking assistance with?",
    }

    compiled = {
        **(partial['params'] if partial else {}),
        **parameters
    }

    valid = {
        param:compiled[param]
        for param in params.keys()
        if param in compiled
    }

    has_all_params = len(valid.keys()) == len(params.keys())
    already_sent = partial['state'].get('sent') == True if partial else False

    if len(args)> 0 and args[0] == "help":
        if already_sent:
            return "\n".join([
                "Contact request already created with this thread."
                "Please start a new thread with",
                "> @Bot contact"
            ])
        return "\n".join([
            "Data so far:",
            *[f"> {key}: {value}" for key, value in partial['params'].items()]
        ])

    if already_sent: return

    if has_all_params: # Have all the keys
        if partial:
            partial['state']['sent'] = True

        email.send_message(
            email= valid.get("email"),
            name= valid.get("name"),
            service_type= valid.get("service-type")
        )
        return "Thanks for the notification request!"

    if already_sent:
                return

    if not partial:
        partial = {"command_name": "contact","params":valid,'state':{}}
        partial_commands[_get_thread(payload)] = partial
    else:
        partial['params'] = valid

    if len(args) < 1: # Create partial and return instructions
        return (
            "\n".join([
                "Thanks for wanting to provide feedback to Taos."
                "Please provide the following information.",
                *[
                    f"- {param}: {help_text}"
                    for param, help_text in params.items()
                ],
                "Example:",
                "> --email devopsnow@taos.com",
                "You can also say help for more information."
            ])
        )

    if parameters:
        return f"Thanks for providing: {', '.join(parameters.keys())}."

botcommands = {
    "about": _parse_about,
    "bio": _parse_bio,
    "contact": _parse_contact
}

def run_bot():
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()

if __name__ == "__main__":
    run_bot()
