import os
import json
import requests
from datetime import datetime, timedelta, timezone


def fetch_json_response(url):
    cwd = os.getcwd()
    
    # Construct the file path relative to the current working directory
    file_path = os.path.join(cwd, '.config.json')

    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
        username = config['username']
        password = config['password']

    # Request headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the GET request
    response = requests.get(url, auth=(username, password), headers=headers)
    global time_ago,assignee_name,latest_comment_author
    # Check the response status
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()
        latest_comment = ""  # Initialize with default value
        latest_comment_time = ""  # Initialize with default value
        time_ago=""
        latest_comment_author = "" 
        assignee_name="No Assignee"
        
        if 'fields' in json_response:
            fields = json_response['fields']
            
            if 'comment' in fields:
                comments = fields['comment']['comments']
                print('comments-', comments)
                
                if comments:
                    # Sort the comments by created time in descending order
                    sorted_comments = sorted(comments, key=lambda c: c['created'], reverse=True)
                    latest_comment = sorted_comments[0]['body']
                    latest_comment_time = sorted_comments[0]['created']
                    latest_comment_author = sorted_comments[0]['author'].get('displayName', '')
                    
                    print("Latest Comment:", latest_comment)
                    print("Time:", latest_comment_time)
                    print("Commenter ID:", latest_comment_author)

                    # Modify Commenter ID to have the first letter capitalized and strip off the part after "."
                    latest_comment_author = latest_comment_author.split(".")[0].capitalize()
                    print("Modified Commenter ID:", latest_comment_author)

                     # Calculate time difference
                    current_time = datetime.now(timezone.utc)
                    comment_time = datetime.strptime(latest_comment_time, "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(timezone.utc)
                    print(current_time)
                    print(comment_time)
                    time_difference = current_time - comment_time
                    print('time_difference-',time_difference)
                    
                    # Calculate days, hours, and minutes
                    days = time_difference.days
                    print(days)
                    hours = time_difference.seconds // 3600
                    minutes = (time_difference.seconds // 60) % 60
                    
                    
                    if days ==1:
                        time_ago = f"{days} day ago"
                    elif days >1:
                        time_ago = f"{days} days ago"    
                    elif hours == 1:
                        time_ago = f"{hours} hour ago"
                    elif hours > 1:
                        time_ago = f"{hours} hours ago"    
                    elif minutes == 1:
                        time_ago = f"{minutes} minute ago"
                    elif minutes > 1:
                        time_ago = f"{minutes} minutes ago"    
                    else: time_ago = ''  
                    
                    print("Time ago:", time_ago)
                    if 'assignee' in fields:
                        assignee = fields['assignee']
                    
                        if assignee:
                            assignee_name = assignee['displayName']
                            # print("Assignee:", assignee_name)
                        else:
                            assignee_name = "No assignee"
                            # print("No assignee")
                    else:
                         print("No assignee")
                    
                    
                else:
                    print("No comments")
                    latest_comment_time = 0
            else:
                # print("No comments")
                latest_comment_time = 0

            if 'status' in fields:
                        status = fields['status']['name']
                        print("status",status)
                        return True, status, latest_comment, time_ago,assignee_name, latest_comment_author
            else:
                        print("Status not found")
           
        else:
            print("Fields not found")
    else:
        print("Failed to fetch JSON. Status code:", response.status_code)
        print("Error message:", response.text)
    
    return False, False, False, False, False, False

# Example usage
# url = "https://esams.atlassian.net/rest/api/2/issue/ES-3"
# json_response = fetch_json_response(url)

# if json_response[0]:
#     print("JSON response received")
#     # print(json_response)
# else:
#     print("JSON response not received")
