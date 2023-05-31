from django.shortcuts import render

import speech_recognition as sr

import pyttsx3
import os
#import azure.cognitiveservices.speech as speechsdk
from .Jira_ticket import Rest_api_jira_call
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from subprocess import Popen
#from jira_api import Rest_api_jira_call




def openapp(request):
    return render(request, 'openapp.html')


def chatbot(request):
    from .speech_recognition1 import recognize_from_microphone

    if request.method == 'POST':
        if 'voice_data' in request.POST:
            # Handle voice input
            voice_data = request.POST['voice_data']
            print(voice_data)
            # text_result = recognize_from_microphone()
            # print(text_result)
            if voice_data:
                # Process the text result and generate a response
                response = process_response(voice_data)
            else:
                response = "Sorry, I couldn't recognize your speech."

            # response = str(response)

            data = {'response': response}

            print("data", data)

            # response = process_response(voice_data)

            voice_output(data["response"])
            return JsonResponse(data)

        else:
            # Handle text input
            message = request.POST['message']
            print("message in view.py", message)
            response = process_response(message)
            data = {'response': response}
            print("data", data)
            voice_output(data["response"])
            #value = data.get('response')
            return JsonResponse(data)

    return render(request, 'chatbot_blue.html')



def process_response(message):
    # if message == 'Hello.':
    #    return 'Hi there!'

    # elif message.lower() in ["yes.", "i want to create a jira ticket."]:
    #    return "Could you please tell me the project name?"

    # else:
    #    return "I'm sorry, I didn't understand. Please type something!"

    if message.lower() in ["hello.", "hi.", "good morning.", "what's up", "yo", "how are you", "how are you?", "how are you.", "how r u?"]:
        return 'Hi, I am a Ally Voice Bot. How can I help you!'

    elif message.lower() in ["i want to create jira ticket.","create jira ticket.", "create a ticket.", "start a new ticket.", "open a jira ticket", "make a jira ticket", "report a bug", "start a ticket", "start new ticket", "a jira ticket", "initiate a jira ticket.", "enerate a Jira ticket.", "set up a jira ticket.", "establish a jira ticket.", "craft a jira ticket.", "begin a jira ticket.", "create a new jira task.", "Set up a new Jira ticket.", "I want to create JIRA ticket. "]:
        return "Sure. Could you please tell me the issue details!"

    elif ("I have an issue" in message) or ("I am working on" in message) or ("I am facing issue" in message) or ("I'm facing issue" in message):
        print("Inside the Issue detail condition")
        response = jiraApi(message)
            #response = {'response': response}
        return response
            


#############
# Furture Improvement:
# Return response 'Requesting details' & capturing & creating jira ticket
#############

    elif message.lower() in ["fine.", "i am good.", "i am doing good.", "i'm good."]:

        return "Great! How can I help you?"

    elif message.lower() in ["thank you.", "thanks a lot.", "appreciate it."]:

        return "You're welcome! If you need any further assistance, feel free to ask."

    else:

        return "I'm sorry, but I couldn't understand your request. Could you please rephrase or provide more information?"


def voice_output(request):

    engine = pyttsx3.init()

    engine.say(request)
    engine.runAndWait()


def jiraApi(request):

    #if ("I have an issue" in message) or ("I am working on" in message) or ("I am facing issue" in message):
    print("matched! for creating jira ticket using description")
    description1 = request
    summary1 = "TestfromPython-1"
    print(description1, summary1)
    #import json
    result = Rest_api_jira_call(summary1, description1)
    #result1, result2, result3 = Rest_api_jira_call(summary1, description1)
    print("result1:", result)
    #print("result2:", result2)
    #print("result3", result3)
    success = 0

    if (success == 0):
        # elif (message == "No. You can proceed with the same." or message == "No.You can proceed with the same." or message == "You can proceed with the same." or message == "Issue type is fine." or message == "Go ahead." or message == "No problem. Go ahead." or message == "No problem Go ahead."):
        #response = "Sure. Please allow me sometime to generate JIRA ticket. I will update soon."
        #return(result1,result2)
        #result = "Jira Ticket created successfully"
        
        return result
        #response = result1
        

        #response = result2
        


        print(result)


#    from .speech_recognition1 import recognize_from_microphone

#    message = recognize_from_microphone()
#    print(speech_recognition_result)
    # response = process_response(speech_recognition_result)
    # data = {'result': response}
    # return JsonResponse(data)

#    if request.method == 'POST':
#        voice_data = request.POST.get('voice_data')

    # Process the voice data and generate a response
#        response = process_response(voice_data)
#        print(response)

    # Create a dictionary with the response
#        data = {'result': response}

#        return JsonResponse(data)

    # voice_i = speech_reco
    # print (process1);

# def send_message(request):
#    if request.method == 'POST':
#        message = request.POST.get('message')
    # Process the message and generate a bot response
#        response = process_response(message)
#        return JsonResponse({'response': response})

#   return render(request, 'chatbot.html')
