from django.shortcuts import render
import speech_recognition as sr
from .Jira_ticket import Rest_api_jira_call
from django.http import JsonResponse
from .openAi_extract_detail import open_api_call
#from .response_handler import process_response
from .check_input_for_details import check_input
from .Intent_extraction import intent_extraction
from .Random_query_handler import random_query_handler
from .code_testing import check_if_all_details_are_present


previous_response = ""
sum,des,proj = "","",""

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
            output = flow_control(voice_data)
           
            
        else:
            # Handle text input
            message = request.POST['message']
            print("message in text format received msg:", message)
            output = flow_control(message)
        response = output
        previous_response = output
        data = {'response': response, 'voice_output':True}
        
        #voice_output(data["response"])              #testing change
        return JsonResponse(data)
    return render(request, 'chatbot_blue.html')
    
def flow_control(voice_data):
    global previous_response
    global proj
    global sum
    global des

    if previous_response in ['Please provide the details for your ticket']:
        all_details_flag,missing_details_list = check_variables(proj,sum,des)

        #print("missing details list" +missing_details_list)
        if all_details_flag == 1:
            print("positive all details flag")
            issue_key=Rest_api_jira_call(proj,sum,des)
            url = 'https://jira.nagarro.com/rest/api/2/issue/'+issue_key
            output = 'Ticket created successfully,'+' Ticket number is: '+issue_key
            #Link for ticket: '+url
            return output
        
        else:
            print("in missing details list else loop")
            for items in missing_details_list:
                output ='Please provide the required details for:'+items
                print("output in missing_details_list"+output)
            return output

    elif previous_response.startswith("Please provide the required details for:"):
        #get project,sum,des from user input//incomplete code
        #proj,sum,des
        text = voice_data+proj+sum+des
        proj,sum,des = open_api_call(text)
        issue_key=Rest_api_jira_call(proj,sum,des)
        url = 'https://jira.nagarro.com/rest/api/2/issue/'+issue_key
        output = 'Ticket created successfully,'+' Ticket number is: '+issue_key
        # Link for ticket: '+url    
        return output
    else:
        intent= intent_extraction(voice_data)   #Get intent,true or false
        print(intent)
        if intent == 'True':                             #user wants to create a message
            if check_if_all_details_are_present(voice_data):         #user has given all details along with +ive intent
                print("positive intent loop")
                proj,sum,des = open_api_call(voice_data)   #if any detail is given by user input already then extract it and if some required field is missing then request it
                print(proj,sum,des) 
                #check if all are given in input,or few are given
                all_details_flag,missing_details_list = check_variables(proj,sum,des)

                #print("missing details list" +missing_details_list)
                if all_details_flag == 1:
                    print("positive all details flag")
                    issue_key=Rest_api_jira_call(proj,sum,des)
                    url = 'https://jira.nagarro.com/rest/api/2/issue/'+issue_key
                    output = 'Ticket created successfully,'+' Ticket number is: '+issue_key
                    #Link for ticket: '+url
                    return output
                
                else:
                    print("in missing details list else loop")
                    for items in missing_details_list:
                        output ='Please provide the required details for:'+items
                        print("output in missing_details_list"+output)
                    return output
            else:
                return 'Please provide the details for your ticket'
        #output = process_response(voice_data)
        else:                                   #user does not want to create a msg and do small talk
            #send a normal reply to user from openAi
            output = random_query_handler(voice_data)
            return output

#Get user confirmation for ticket creation
def confirm_user_input():
    return 'confirm'


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
        output = 'Ticket created successfully,'+' Ticket number is: '+issue_key 
        # Link for ticket: '+url
        print(output)
        previous_response = ""    
        return output
           

def check_variables(project, summary, description):
    if project and summary and description:
        # All variables are present
        all_present = 1
        print("All variables are present.")
        return all_present,[project,summary,description]
    else:
        # Determine which variable(s) is/are missing
        missing_variables = []
        if not project:
            all_present = 0
            missing_variables.append("project")
        if not summary:
            all_present = 0
            missing_variables.append("summary")
        if not description:
            all_present = 0
            missing_variables.append("description")

        # Print the missing variables
        print("The following variable(s) are missing:")
        for variable in missing_variables:
            print(variable)
        
        return all_present,missing_variables





    



