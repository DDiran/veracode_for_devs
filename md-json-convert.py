import json
import re
from os import path

def extract_data(file):
    # Initialize a dictionary to store the data
    data = []

    # Regular expression to match a package line
    # package_regex = re.compile(r'\[(.*?)\]\((.*?)\)\s\((.*?)\)\s-\s(.*?)\.')
    package_regex = re.compile(r"- \[(.*)\]\((.*)\) \((\[.*\]\(.*\))\) - (.*)")

    # Regular expression to match a heading line
    heading_regex = re.compile(r"^(#+) (.*)") #r'^(#+)\s(.*?)$'

    # Initialize a variable to keep track of the current categories
    current_category = None
    current_subcategory = None

    with open(file, "r") as f:
        for line in f:
            # Match the line against the heading regex
            heading_match = heading_regex.match(line)
            if heading_match:
                # If the line is a heading line, extract the heading level and name
                heading_level = len(heading_match.group(1))
                heading_name = heading_match.group(2).strip()

                # Set the current categories based on the heading level
                if heading_level == 2:
                    current_category = heading_name
                    current_subcategory = None
                elif heading_level == 3:
                    current_subcategory = heading_name

            # Match the line against the package regex
            package_match = package_regex.match(line)
            if package_match:
                # If the line is a package line, extract the package name, link, author, and description
                package_name = package_match.group(1).strip()
                package_link = package_match.group(2).strip()
                author_name = re.findall(r"\[(.*)\]", package_match.group(3))[0]
                author_profile_link = re.findall(r"\((.*)\)", package_match.group(3))[0]
                description = package_match.group(4).strip()

                # Add the package to the data list with the author and description
                data.append({
                    "name": package_name,
                    "link": package_link,
                    "author": {
                        "name": author_name,
                        "profile_link": author_profile_link
                    },
                    "description": description,
                    "categories": {
                        "category": current_category,
                        "subcategory": current_subcategory
                    }
                })
    return data

def main():
    cur_dir = path.dirname(path.realpath(__file__))
    readme_path = path.join(cur_dir, 'README.md')

    # Call the extract_data function to get the data from the file
    data = extract_data(readme_path)

    # Add a parent key to the data called 'community_integrations'
    data = {'community_integrations': data}

    # Save the data to a JSON file
    with open('community_integrations.json', 'w') as f:
        f.write(json.dumps(data))

if __name__ == "__main__":
    main()
