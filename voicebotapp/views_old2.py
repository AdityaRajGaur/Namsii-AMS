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
application,description,summary,priority = "","","",""

def index(request):
    return render(request, 'index.html')


def chatbot(request):
    global previous_response
    data ={}
    if request.method == 'POST':
        if 'voice_data' in request.POST:
            # Handle voice input
            voice_data = request.POST['voice_data']
            output = flow_control(voice_data)
           
            
        else:
            # Handle text input
            message = request.POST['message']

            output = flow_control(message)
        response = output
        previous_response = output
        data = {'response': response, 'voice_output':True}
        
        #voice_output(data["response"])              #testing change
        return JsonResponse(data)
    return render(request, 'chatbot_blue.html')
    
def flow_control(voice_data):
    global previous_response
    global application
    global description
    global summary
    global priority

    if previous_response in ['Please provide the details for your ticket']:
        
        output = check_det(voice_data)
        return output


        # if check_if_all_details_are_present(voice_data) == 'True':
        #     output = check_det(voice_data)
        #     print("output from check_det",output)
        # else:
        #     output = 'Could you please elaborate the problem you are facing.A brief description is missing!'
        # return output
        # val =check_if_all_details_are_present(voice_data)
        # print("val",val)
        # print('val type:',type(val))
        # if val == 'True':
        #     check_det(voice_data)
        # else:
        #     return '0Please provide the details for your ticket'

        
        # check = check_if_all_details_are_present(voice_data)
        # print('check:',type(check))
        # if check == 'True':         #user has given all details along with +ive intent
        #     result = check_det(voice_data)
        #     output = result
        #     return output
        # else:
        # if check_if_all_details_are_present(voice_data)== 'True':
        #     output = check_det(voice_data)
        
        # return output


    elif previous_response.startswith("Please provide the required details for:") or previous_response in ['Could you please elaborate the problem you are facing.A brief description is missing!']:
        #get project,sum,des from user input//incomplete code
        #proj,sum,des
        text = voice_data+application+description+summary+priority
        application,description,summary,priority = open_api_call(text)
        issue_key=Rest_api_jira_call(application,description,summary,priority)
        url = 'https://jira.nagarro.com/rest/api/2/issue/'+issue_key
        output = 'Ticket created successfully,'+' Ticket number is: '+issue_key
        return output
    else:
        intent= intent_extraction(voice_data)            #Get intent,true or false
        if intent == 'True':   
            print("inside Intent"+intent)                         #user wants to create a message
            check =check_if_all_details_are_present(voice_data)
            if check == 'True':
                print("inside check"+check)         #user has given all details along with +ive intent
                output = check_det(voice_data)
                return output
            else:
                return check_det(voice_data)

                #return 'Please provide the details for your ticket'
                
        #output = process_response(voice_data)
        else:                                   #user does not want to create a msg and do small talk
            #send a normal reply to user from openAi
            output = random_query_handler(voice_data)
            return output

#Get user confirmation for ticket creation
def confirm_user_input():
    return 'confirm'

def check_det(voice_data):

    application,description,summary,priority=open_api_call(voice_data)
    #proj,sum,des = open_api_call(voice_data)   #if any detail is given by user input already then extract it and if some required field is missing then request it
    #check if all are given in input,or few are given
    all_details_flag,missing_details_list = check_variables(application,description,summary,priority)


    if all_details_flag == 1:
        print("all details present")
        issue_key=Rest_api_jira_call(application,description,summary,priority)
        url = 'https://jira.nagarro.com/rest/api/2/issue/'+issue_key
        output = 'Ticket created successfully,'+' Ticket number is: '+issue_key
        return output
    
    else:
        print("some details absent")
        line = 'Please provide the required details for: '
        if len(missing_details_list)>1:
            words = ' and '.join(missing_details_list)
        else:
                words = missing_details_list[0]
                output = line + ' ' + words.capitalize()
        print(output)
        return output


def check_variables(application,description,summary,priority):
    if application and description and summary and priority:
        # All variables are present
        all_present = 1
        print("All variables are present.")
        return all_present,[application,summary,description,priority]
    else:
        # Determine which variable(s) is/are missing
        missing_variables = []
        if not application:
            all_present = 0
            missing_variables.append("application name")
        if not (summary or description):
            all_present = 0
            missing_variables.append("description")
        if not priority:
            all_present = 0
            missing_variables.append("severity")

        # Print the missing variables
        print("The following variable(s) are missing:")
        for variable in missing_variables:
            print(variable)
        
        return all_present,missing_variables





    



