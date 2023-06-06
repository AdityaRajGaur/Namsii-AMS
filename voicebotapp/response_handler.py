##Handle Ticket control process here.

from .Jira_ticket import Rest_api_jira_call

def process_response(message):
    if message.lower() in ["hello.","greetings","hai","haiii","hello","hey.","hey","hi.", "hi","good morning.", "what's up", "yo", "how are you", "how are you?", "how are you.", "how r u?"]:
        return "Hi, I am a Jira Voice Bot. How can I help you!"

    elif message.lower() in ["create jira ticket.","please create a jira ticket","please create a ticket","please create a jira ticket.","create jira ticket","create ticket","i have an issue","i have a issue","raise a ticket","create a jira ticket","i want to create a jira ticket","create a jira ticket.", "create a ticket.", "start a new ticket.", "open a jira ticket", "make a jira ticket", "report bug", "start a ticket", "start new ticket", "a jira ticket", "initiate a jira ticket.","report a bug" "enerate a Jira ticket.", "set up a jira ticket.", "establish a jira ticket.", "craft a jira ticket.", "begin a jira ticket.", "create a new jira task.", "Set up a new Jira ticket.", "I want to create jira ticket. "]:
        return "Sure, Do you want to 'add details'  or proceed with 'default' for now"

    elif message.lower() in ["add details", "add detail"]:
        return "Ok, Please provide project name,description and summary for your ticket."
 
    elif message.lower() in ["default","proceed with default"]:
        response = jiraApi('default')
        print(response)

    elif message.lower() in ["fine.", "i am good.", "i am doing good.", "i'm good."]:
        return "Great! How can I help you?"

    elif message.lower() in ["thank you.", "thanks a lot.", "appreciate it.", "thanks","thank you","thanks."]:
        return "You're welcome! If you need any further assistance, feel free to ask."
    
    elif message.lower() in ["what can you do for me","what can you do for me?","what can you do","what can you do?","help","help"]:
        return "I am a Jira Voice Bot Ally and I can help you create a Jira ticket, you can try instructions like 'Create a Jira Ticket.' "
    else:
        return "I'm sorry, but I couldn't understand. Please re-try or provide more information."      #rephrase-shorten


#default case
def jiraApi(request):

    if request == "default":
        print("matched! for creating jira ticket using description")
        description1 = "Default Ticket created."
        summary1 = "Add summary later"
        project1 = "Add a project later"
        issue_key = Rest_api_jira_call(project1,summary1, description1)
        print("issue_key:", issue_key)
        success = 1

    if (success == 1):
        response = "Jira Ticket created successfully"
        return response