from django.shortcuts import render
import speech_recognition as sr
import pyttsx3
from .Jira_ticket import Rest_api_jira_call
from django.http import JsonResponse
from .openAi_extract_detail import open_api_call
from .response_handler import process_response
from .speech_recognition1 import recognize_from_microphone

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
            #check if previous response was add details then extract details and create ticket
                #project,sum,des  = extract_ticket_details(voice_data)
            if previous_response in ['Ok, Please provide project name,description and summary for your ticket.']:
                print("Get text user inputs for fetching details with message :",voice_data)
                try:
                    proj,sum,des = open_api_call(voice_data)
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
                    data = {'response':output}
                    print(data)
                    previous_response = ""   
                    response = output     
            
            elif voice_data:
                # Process the text result and generate a response
                response = process_response(voice_data)
                
            else:
                response = "Sorry, I couldn't recognize your speech."

            # response = str(response)

            data = {'response': response}

            print("data", data)

            # response = process_response(voice_data)
            previous_response = response
            voice_output(data["response"])
            return JsonResponse(data)

        else:
            # Handle text input
            message = request.POST['message']
            print("message in view.py", message)
            if previous_response in ['Ok, Please provide project name,description and summary for your ticket.']:
                print("Get text user inputs for fetching details with message :",message)
                try:
                    proj,sum,des = open_api_call(message)
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
                    data = {'response':output}
                    print(data)
                    previous_response = ""   
                    response = output             

            else:
                response = process_response(message)

            previous_response = response
            data = {'response': response}
            voice_output(data["response"])
        return JsonResponse(data)

    
    return render(request, 'chatbot.html')
    

def voice_output(request):

    engine = pyttsx3.init()

    engine.say(request)
    engine.runAndWait()