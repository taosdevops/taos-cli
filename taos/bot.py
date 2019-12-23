import os
import slack
from pprint import pprint
from taos import bio, about

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


def _get_thread(payload: dict)-> str:
    data = payload.get("data", {})
    return data.get("thread_ts") or data.get("ts")


def talking_to_me(func):
    def _internal_(**payload):
        # pprint({"Payload": payload})
        data = payload["data"]
        if not bot_string in data.get("text", []):
            return
        return func(**payload)

    return _internal_


def _is_bot(data, **kwargs):
    return "bot_id" in data and data["bot_id"] == bot_data["bot_id"]


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

            if isinstance(response, str):
                response = [response]

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
            print(f"HIT Exception:{e}")

    return _internal_


@slack.RTMClient.run_on(event="message")
@talking_to_me
def processor(**payload):
    data = payload["data"]
    commands = [
        command
        for command, response in botcommands.items()
        if f"{bot_string} {command}" in data.get("text", "")
    ]

    if len(commands) > 0:
        try:
            command_string = data.get("text", "").split(bot_string)[1].strip()
            botcommands[commands[0]](*command_string.split(" "), **payload)
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
    try:
        command_string = data.get("text", "").split(bot_string)[1].strip()
    except IndexError:
        command_string = data.get("text", "").strip()

    botcommands[command_name](
        command_name, *command_string.split(" "), data=data, **payload
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


botcommands = {
    "about": _parse_about,
    "bio": _parse_bio
}

if __name__ == "__main__":
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
