import os
import slack
from pprint import pprint
from taos import bio, about, email
import traceback
from taosdevopsutils.slack import Bot
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
bot = Bot(os.environ["SLACK_API_TOKEN"], logger=logging)

slack_token = os.environ["SLACK_API_TOKEN"]
bot_data = slack.WebClient(token=slack_token).auth_test()
bot_string = f"<@{bot_data['user_id']}>"

bio_users = bio.list_persons()
about_services =[
    service['name'] for service in about.list_services()
    if service.get('name') and service['name'] != ''
]


@bot.register("about")
def _parse_about(command_name, *args, thread_id=None, **payload):
    newline_join = lambda items: "\n".join(items)
    if len(args) < 1:
        bot.partial_commands[thread_id] = {"command_name": "about"}
        return newline_join([
            "Thanks for asking about me.",
            *about.get_about()
        ])

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

@bot.register("bio")
def _parse_bio(command_name, *args, thread_id=None, **payload):
    if len(args) < 1:
        bot.partial_commands[thread_id] = {"command_name": "bio"}
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


@bot.register("contact")
@bot.fetch_partial
def _parse_contact(command_name, *args, thread_id=None, parameters=None, partial=None):
    print("Partial",partial)
    print("Args", args)
    print("Parameters", parameters)
    print("threadid", thread_id)
    assert thread_id
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
        bot.partial_commands[thread_id] = partial
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
    bot.start()

if __name__ == "__main__":
    run_bot()
