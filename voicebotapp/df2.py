import dialogflow
from google.cloud import dialogflow_v2beta1 as dialogflow
import os

def chat_view(message):

    print("inside chat_view", message)
    # gcp authentication and project variables
    GOOGLE_AUTHENTICATION_FILE_NAME = "dialogflow.json"
    current_directory = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
    GOOGLE_PROJECT_ID = "handy-digit-387917"
    session_id = "12345"
    context_short_name = "no_name"

    # handle input value depending on text input
   
    input_value = message
    context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + \
               context_short_name.lower()

    #set up parameters and request to call dialogflow detectintent endpoint
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
    print('response inside chatview is: ',response.query_result.fulfillment_text)

    #return httpresponse received from the detectintent API
    return response.query_result.fulfillment_text


        
def detect_intent_with_parameters(project_id, session_id,  language_code,knowledge_base_id, user_input):

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
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    query_params = dialogflow.QueryParameters(
            knowledge_base_names=[knowledge_base_path]
        )
    
    if response.query_result.fulfillment_text :
        1
        # print('Fulfillment text: {}\n'.format(
        # response.query_result.fulfillment_text))
        
    else:
        for text in [user_input,]:
            text_input = dialogflow.TextInput(text=text, language_code=language_code)
        
            request = dialogflow.DetectIntentRequest(
            session=session, query_input=query_input, query_params=query_params
        )
        response = session_client.detect_intent(request=request)
        # Process knowledge base answers
        print("Knowledge results:")
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        knowledge_answers = response.query_result.knowledge_answers
        for answers in knowledge_answers.answers:
            print(" - Answer: {}".format(answers.answer))
            print(" - Confidence: {}".format(answers.match_confidence)) 
        
    
    
    # knowledge_answers = response.query_result.knowledge_answers
    # for answers in knowledge_answers.answers:
    #         print(" - Answer: {}".format(answers.answer))
    #         print(" - Confidence: {}".format(answers.match_confidence))
    

    return response
  
    
chat_view('What are the things that you can do for me')


