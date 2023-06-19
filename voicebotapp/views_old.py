from django.shortcuts import render
import speech_recognition as sr
from .Jira_ticket import Rest_api_jira_call
from django.http import JsonResponse
from .openAi_extract_detail import open_api_call
from .response_handler import process_response
# added by Surabhi
import dialogflow
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
import os
import time
from google.cloud import dialogflow_v2beta1 as dialogflow
import uuid
from django.contrib.sessions.backends.db import SessionStore


previous_response = ""
# session_id = str(uuid.uuid4())
session_key = ""


def index(request):
    return render(request, 'index.html')


def chatbot(request):
    global previous_response
    data = {}
    # print(request)
    # session_id = 'voice_data'.session.cycle_key()
    global session_id
    session_id = '123'
    # print('session id: ', session_id)
    if request.method == 'POST':
        if 'voice_data' in request.POST:
            # Handle voice input
            voice_data = request.POST['voice_data']

            print("message in test_code.py 28", voice_data)
            
            print('session id: ', session_id)
            output = chat_view(voice_data, session_id)
            print('Output Line 30', output)

            if 'Please give me a moment to process the details.' in output:

                voice_data = output.replace(
                    'Please give me a moment to process the details.', '')
                print("Inside Output 36", voice_data)
            #    add_waiting_time (request)
                output = open_ai_and_jira_call(voice_data)
            else:
                print("Not Inside Output")
                # output = chat_view(voice_data)
                # print('Output line 32',output)

        else:
            # Handle text input
            message = request.POST['message']

            if 'Please give me a moment to process the details.' in message:
                message = message.replace(
                    'Please give me a moment to process the details.', '')
                print("message on line 50", message)
                output = open_ai_and_jira_call(message)
            else:
                output = chat_view(message, session_id)
                print('Output line 43', output)
        response = output
        previous_response = output
        data = {'response': response, 'voice_output': True}

        # voice_output(data["response"])  #testing change
        return JsonResponse(data)
    return render(request, 'chatbot_blue.html')


def open_ai_and_jira_call(user_input):
    global previous_response
    print("56 Get text user inputs for fetching details with message :", user_input)

    try:
        proj, des, sum, prt = open_api_call(user_input)
        print('project,summary and description from open ai call is: ', proj, sum, des, prt)
    except:
        print('Issue with the open api call')
        return 'Error fetching details from openAI api'
    try:
        issue_key = Rest_api_jira_call(proj, sum, des)
        # issue_key = '1234'
        print('inside jira create func')
    except:
        print("Error connecting via JIRA api")
        return 'Error connecting to JIRA api'
    if issue_key:
        url = 'https://jira.nagarro.com/browse/'+issue_key
        output = 'Please give me a moment to process the details for your issue-   \n\n' + user_input  + \
            '\n\n Ticket created successfully,'+' Ticket number is: '+issue_key
        print(output)
        previous_response = ""
        return output


# Added by Surabhi

def chat_view(message, session_id):

    print("inside chat_view", message)
    # gcp authentication and project variables
    GOOGLE_AUTHENTICATION_FILE_NAME = "dialogflow.json"
    current_directory = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
    GOOGLE_PROJECT_ID = "handy-digit-387917"
    # session_id=session_id
    context_short_name = "no_name"
    session_id = session_id
    print('session id117: ', session_id)
    # handle input value depending on text input

    input_value = message
    context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + \
        context_short_name.lower()

    # set up parameters and request to call dialogflow detectintent endpoint
    # parameters = dialogflow.types.struct_pb2.Struct()
    # context_1 = dialogflow.types.context_pb2.Context(
    #     name=context_name,
    #     lifespan_count=6,
    #     parameters=parameters
    # )
    # query_params_1 = {"contexts": [context_1]}
    language_code = 'en'

    # call dialogflow detectintent endpoint and save result in response
    response = detect_intent_with_parameters(
        project_id=GOOGLE_PROJECT_ID,
        session_id=session_id,
        # query_params=query_params_1,
        language_code=language_code,
        knowledge_base_id='NjY2OTEzNzgwNjA1NDM5MTgwOA',
        user_input=input_value
    )
    # print('response inside chatview is: ',response.query_result.fulfillment_text)

    # return httpresponse received from the detectintent API
    return response.query_result.fulfillment_text


def detect_intent_with_parameters(project_id, session_id,  language_code, knowledge_base_id, user_input):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text = user_input

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    # Added for reading resposes from Knowledge Base
    knowledge_base_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
        project_id, knowledge_base_id
    )
    context_short_name = "no_name"
    context_name = "projects/" + project_id + "/agent/sessions/" + session_id + "/contexts/" + \
        context_short_name.lower()
    # parameters = dialogflow.types.Struct()
    # context_1 = dialogflow.types.context_pb2.Context(
    #     name=context_name,
    #     lifespan_count=6,
    #     parameters=parameters
    # )
    # query_params = {"contexts": [context_1]}

    # request = dialogflow.DetectIntentRequest(
    #         session=session, query_input=query_input, query_params=query_params
    #     )
    # response = session_client.detect_intent(request=request)

    response = session_client.detect_intent(
        session=session, query_input=query_input
        # query_params=query_params
    )

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence
    ))
    print("Fulfillment text: {}\n".format(
        response.query_result.fulfillment_text))

    if response.query_result.fulfillment_text:
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        length = len(response.query_result.fulfillment_text)
        print('Length is', length)

    else:
        for text in [user_input,]:
            query_params = dialogflow.QueryParameters(
                knowledge_base_names=[knowledge_base_path]
            )
            text_input = dialogflow.TextInput(
                text=text, language_code=language_code)

            request = dialogflow.DetectIntentRequest(
                session=session, query_input=query_input, query_params=query_params
            )
        response = session_client.detect_intent(request=request)
        # Process knowledge base answers
        print("Knowledge Fulfillment text: {}\n".format(
            response.query_result.fulfillment_text))
        knowledge_answers = response.query_result.knowledge_answers
        # length = len(knowledge_answers)
        print('knowledge_answers',knowledge_answers)
        print(len(response.query_result.fulfillment_text))
        reponse = response.query_result.fulfillment_text
        length = len(response.query_result.fulfillment_text)
        # reset_dialogflow_context()
        session_id = session_id + '1'
        print('Line 228',session_id)
        print('Length is', length)

    if length > 1:
        return response
    else:
        return 'Sorry, can you please say that again.'
    # knowledge_answers = response.query_result.knowledge_answers
    # for answers in knowledge_answers.answers:
    #         print(" - Answer: {}".format(answers.answer))
    #         print(" - Confidence: {}".format(answers.match_confidence))


def reset_dialogflow_context():
    project_id = "handy-digit-387917"
    session_id = str(uuid.uuid4())
    print('inside reset context', session_id)
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(project_id, session_id)

    # Construct a reset context request
    reset_contexts_request = dialogflow.types.ResetContextsRequest(
        session=session_path
    )

    # Send the reset context request to Dialogflow
    session_client.reset_contexts(reset_contexts_request)
