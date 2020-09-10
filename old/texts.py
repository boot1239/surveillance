from constants import *

process_error_response = (
    'The command "{command}" is not recognized. Try writing "help" for a '
    'list of commands.'
)
process_not_clickable_response = (
    "The command \"{command}\" doesn't support clicking."
)

help_description = 'Lists all available commands'
_help_response = (
    'Thank you for using Hacker Console version {version} help '
    'command.\nBelow is a list of available commands: \n\n{cmds}'
)
help_response = _help_response.format(version=CONSOLE_VERSION, cmds='{cmds}')

search_description = 'Search for entries in the database.'
search_error = 'No results found for "{criteria}."'

detail_description = 'Details a person in the database.'
detail_error = 'No person found for "{criteria}."'

time_description = 'Shows current time.'
time_response = 'Current time is {time}.'
