from django.shortcuts import render
import speech_recognition as sr
from .Jira_ticket import Rest_api_jira_call
from django.http import JsonResponse
from .openAi_extract_detail import open_api_call
from .response_handler import process_response

previous_response = ""

def index(request):
    return render(request, 'index.html')


def chatbot(request):
    global previous_response
    data ={}
    if request.method == 'POST':
        if 'voice_data' in request.POST:
            # Handle voice input
            voice_data = request.POST['voice_data']
            print(voice_data)
            if previous_response in ['Ok, Please provide project name,description and summary for your ticket.']:
               output = open_ai_and_jira_call(voice_data)                
            else:
                output = process_response(voice_data)
            
        else:
            # Handle text input
            message = request.POST['message']
            print("message in test_code.py", message)
            if previous_response in ['Ok, Please provide project name,description and summary for your ticket.']:
               previous_response = ""
               output = open_ai_and_jira_call(message)       
            else:
                output = process_response(message)
        response = output
        previous_response = output
        data = {'response': response, 'voice_output':True}
        
        #voice_output(data["response"])              #testing change
        return JsonResponse(data)
    return render(request, 'chatbot_blue.html')
    

def open_ai_and_jira_call(user_input):
    global previous_response
    print("Get text user inputs for fetching details with message :",user_input)
    try:
        proj,sum,des = open_api_call(user_input)
        print('project,summary and description from open ai call is: ', proj,sum,des)
    except:
        print('Issue with the open api call')
        return 'Error fetching details from openAI api'
    try:
        issue_key = Rest_api_jira_call(proj,sum,des)  
        print(issue_key)
    except:
        print("Error connecting via JIRA api")
        return 'Error connecting to JIRA api'
    if issue_key:
        url = 'https://jira.nagarro.com/rest/api/2/issue/'+issue_key
        output = 'Ticket created successfully,'+' Ticket number is: '+issue_key+' Link for ticket: '+url
        print(output)
        previous_response = ""    
        return output
           



    



