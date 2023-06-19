import requests
import json
import os


def Rest_api_jira_call(project,summary,description, priority):
# Jira API endpoint and authentication details
    url = "https://esams.atlassian.net/rest/api/2/issue/"
    print("inside the function fro rest api call")
    print(project,summary,description)
    # Get the current working directory
    cwd = os.getcwd()
    print(cwd)

# Construct the file path relative to the current working directory
    file_path = os.path.join(cwd, '.config.json')
    print(file_path)

    with open(file_path,'r') as config_file:
        config = json.load(config_file)
        username = config['username']
        password = config['password']

# Request headers
    headers = {
        "Content-Type": "application/json"
    }

# Request payload for creating the Jira issue
    payload = {
        "fields": {
            "project": {
                "id": "10000"
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "id": "10004"
            },
        
            "customfield_10033":{ "value":priority}

        }
    }

# Make the API request
    response = requests.post(url, auth=(username, password), headers=headers, json=payload)

# Check the response status
    if response.status_code == 201:
        #print("Issue created successfully.")
        issue_key = response.json()["key"]
        print("Issue Number:", issue_key)
        link= "https://esams.atlassian.net/browse/"+ issue_key
        return issue_key
    else:
        print("Failed to create issue. Status code:", response.status_code)
        print("Error message:", response.text)
        return response.text
