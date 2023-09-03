# Parse API blueprint files to auto-generate Python code

Uses drafter (https://github.com/apiaryio/drafter) to parse APIB and create JSON representation which is then parsed 
using Pydantic models.

# 
# create yml for each apib file

    find . -iname "*.apib" -exec sh -c 'drafter -f json "$1" -o "${1%.apib}.yml"' sh {} \;

## read API blueprints as dict

## read dict

## understand the structure of the dict and parse