import json
import re
from os import path

def extract_data(file):
    # Initialize a dictionary to store the data
    data = []

    # Regular expression to match a package line
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

def save_to_json(data):
    # Community-feed path
    json_path = path.join(path.dirname(path.realpath(__file__)), 'community-feed')

    # Create a dictionary to store the category files
    category_files = {}

    # Save the entire dataset to a JSON file
    with open(path.join(json_path, 'community_integrations.json'), 'w') as f:
        f.write(json.dumps(data))

# Loop through the JSON entries and group them by category
    for entry in data['community_integrations']:
        category = entry['categories']['category']

        # Create a new file for the category if it doesn't exist
        if category not in category_files:
            category_file_path = path.join(json_path, f"{category}.json")
            category_files[category] = open(category_file_path, "w")
        
        # Write the entry to the corresponding category file
        json.dump(entry, category_files[category])
        category_files[category].write("\n")

    # Close all the category files
    for f in category_files.values():
        f.close()

# def publish_to_remote_repo(category_files):
#     # Push the category files to the remote repository
#     repo_owner = "your-username"
#     repo_name = "your-repo"
#     branch_name = "main"
#     commit_message = "Add category files"

#     base_url = "https://api.github.com"
#     headers = {
#         "Authorization": f"token {access_token}",
#         "Accept": "application/vnd.github.v3+json"
#     }

#     for category, f in category_files.items():
#         # Read the category file data
#         f.seek(0)
#         file_data = f.read()

#         # Create the file on the remote repository
#         url = f"{base_url}/repos/{repo_owner}/{repo_name}/contents/{category}.json"
#         data = {
#             "message": commit_message,
#             "content": file_data,
#             "branch": branch_name
#         }
#         response = requests.put(url, headers=headers, json=data)

#         # Check if the request was successful
#         if response.status_code != 201:
#             print(f"Failed to create file for category {category}: {response.json()['message']}")    

def main():
    readme_path = path.join(path.dirname(path.realpath(__file__)), 'README.md')

    # Call the extract_data function to get the data from the file
    data = extract_data(readme_path)

    # Add a parent key to the data called 'community_integrations'
    data = {'community_integrations': data}

    # Save the entire dataset to a JSON file
    save_to_json(data)

if __name__ == "__main__":
    main()
