import re
import sys


MODULE_REGEX = r'^[a-z][_a-z0-9]+$'

tool_name = '{{ cookiecutter.tool_name }}'

if not re.match(MODULE_REGEX, tool_name):
    print('ERROR: %s is not a valid tool name! Regex: \'^[a-z][_a-z0-9]+$\'' % tool_name)

    # exits with status 1 to indicate failure
    sys.exit(1)
