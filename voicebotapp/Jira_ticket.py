import requests

import json

import os





def Rest_api_jira_call(application,description,summary,priority):

# Jira API endpoint and authentication details

    url = "https://jira.nagarro.com/rest/api/2/issue/"

    print("inside the function for rest api JIRA call")

    print(application,description,summary,priority)

    # Get the current working directory

    cwd = os.getcwd()

    print(cwd)




# Construct the file path relative to the current working directory

    file_path = os.path.join(cwd, 'config.json')

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

                "id": "20351"

            },

            "summary": summary,

            "description": description,

            "issuetype": {

                "id": "1"

            },

       

            "customfield_28741":{ "value":"External Testing"},





            "customfield_10023": { "value":"Oversight"},

 




            "customfield_28740": { "value":"To Be Assigned"},

 




            "customfield_10015": { "value":priority}        #priority




        }

    }




# Make the API request

    response = requests.post(url, auth=(username, password), headers=headers, json=payload)

    print(payload)




# Check the response status

    if response.status_code == 201:

        #print("Issue created successfully.")

        issue_key = response.json()["key"]

        print("Issue Number:", issue_key)

        link= "https://jira.nagarro.com/browse/"+ issue_key

        return issue_key

    else:

        print("Failed to create issue. Status code:", response.status_code)

        print("Error message:", response.text)

        return response.text