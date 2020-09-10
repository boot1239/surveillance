from datetime import datetime
import re

from texts import *

from database.app import search_person_any, search_person_full_name


class CommandResponse:
    def __init__(self, message, clickable=False):
        self.message = message
        self.clickable = clickable


def process_command(command, clicked=None):
    prefix, args = command, ''
    if clicked:
        prefix, args = 'search', command
    if len(re.findall(r'\w+', command)) > 1:
        prefix, args = command.split(maxsplit=1)
    if prefix in available_commands:
        return available_commands[prefix]['fnc'](args)
    return CommandResponse(process_error_response.format(command=command))


def help_command(args):
    return CommandResponse(
        help_response.format(cmds='\n'.join(iterate_commands()))
    )


def iterate_commands():
    for cmd, cmd_details in sorted(available_commands.items()):
        yield f'{cmd} \t\t---\t\t {cmd_details["description"]}'


def time_command(args):
    current_time = datetime.now().strftime('%H:%M:%S')
    return CommandResponse(time_response.format(time=current_time))


def search_command(args):
    split = args.split(' ')
    if len(split) == 2:
        persons = search_person_full_name(*split)
    else:
        persons = search_person_any(args)

    num_entries = len(persons.all())
    if num_entries < 1:
        return CommandResponse(search_error.format(criteria=args))

    if num_entries == 1:
        return detail_command(args)

    citizens = ''.join(
        f"{person.citizen_id} - {person.first_name} {person.last_name}\n"
        for person in persons
    )
    return CommandResponse(
        f'Citizen ID - Name \n{citizens}'
        f'{num_entries} results '
        f'found when searching for "{args}".',
        clickable=True,
    )


def detail_command(args):
    split = args.split(' ')
    if len(split) == 2:
        persons = search_person_full_name(*split)
    else:
        persons = search_person_any(args)

    num_entries = len(persons.all())
    if num_entries < 1:
        return CommandResponse(search_error.format(criteria=args))

    if num_entries > 1:
        return search_command(args)

    person = persons.one()
    return CommandResponse(
        f'Showing detailed information of citizen {person.citizen_id}'
        f' - {person.first_name} {person.last_name}:\n'
        f'Cool',
        clickable=True,
    )


available_commands = {
    'help': {
        'fnc': help_command,
        'description': help_description,
    },
    'time': {
        'fnc': time_command,
        'description': time_description,
    },
    'search': {
        'fnc': search_command,
        'description': search_description,
    },
    'detail': {
        'fnc': detail_command,
        'description': detail_description,
    }
}
