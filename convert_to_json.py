# Python script to parse through each bullet point in the README.me file and convert it to JSON

import json
import re
from os import path

cur_dir = path.dirname(path.realpath(__file__))
readme_path = path.join(cur_dir, 'README.md')

# Open the README.me file
with open(readme_path, 'r') as f:
    # Read the file
    data = f.read()

# Create a list of links for each bullet point
# Example: - [Bitrise-step-veracode-scan](https://github.com/psoladoye-geotab/bitrise-step-veracode-scan) ([Psoladoye-geotab](https://github.com/psoladoye-geotab/)) - add Veracode scanning to Bitrise CI.

# Regex to match the links
regex = r'\[(.*?)\]\((.*?)\)\s\((.*?)\)\s-\s(.*?)\.'

# Find all the links
regex = re.findall(regex, data)

# For each list item, create a dictionary with the link name, link, author, and description
regex = [{'name': item[0], 'link': item[1], 'author': item[2], 'description': item[3]} for item in regex]

json_data = json.dumps(regex)

# Write the JSON to a file
with open('links.json', 'w') as f:
    f.write(json_data)
