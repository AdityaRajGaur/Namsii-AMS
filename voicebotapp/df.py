import dialogflow
import dialogflow_v2 as dialogflow
import os




    
    
        # call dialogflow detectintent endpoint and save result in response 
    
# print('response inside chatview is: ',response.query_result.fulfillment_text)

    #return httpresponse received from the detectintent API
# return response.query_result.fulfillment_text

def detect_intent_knowledge(
    project_id, session_id, language_code, knowledge_base_id, texts
):
    """Returns the result of detect intent with querying Knowledge Connector.

    Args:
    project_id: The GCP project linked with the agent you are going to query.
    session_id: Id of the session, using the same `session_id` between requests
              allows continuation of the conversation.
    language_code: Language of the queries.
    knowledge_base_id: The Knowledge base's id to query against.
    texts: A list of text queries to send.
    """
    from google.cloud import dialogflow_v2beta1 as dialogflow

    session_client = dialogflow.SessionsClient()

    session_path = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session_path))
    print('Texts :',texts)
    
    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        print('Text input:',text_input)
        query_input = dialogflow.QueryInput(text=text_input)

        knowledge_base_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
                project_id, knowledge_base_id
            )

        query_params = dialogflow.QueryParameters(
                knowledge_base_names=[knowledge_base_path]
            )

        request = dialogflow.DetectIntentRequest(
                session=session_path, query_input=query_input, query_params=query_params
            )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
                "Detected intent: {} (confidence: {})\n".format(
                    response.query_result.intent.display_name,
                    response.query_result.intent_detection_confidence,
                )
            )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        print("Knowledge results:")
        knowledge_answers = response.query_result.knowledge_answers
        # for answers in knowledge_answers.answers:
        #     print(" - Answer: {}".format(answers.answer))
        #     print(" - Confidence: {}".format(answers.match_confidence))

message = "What are the things that you can do for me"
        # gcp authentication and project variables
GOOGLE_AUTHENTICATION_FILE_NAME = "dialogflow.json"
current_directory = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

GOOGLE_PROJECT_ID = "handy-digit-387917"
session_id = "12345"
context_short_name = "no_name"

        # handle input value depending on text or file input
    
input_value = message
context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + \
                context_short_name.lower()

        #set up parameters and request to call dialogflow detectintent endpoint
parameters = dialogflow.types.struct_pb2.Struct()
context_1 = dialogflow.types.context_pb2.Context(
            name=context_name,
            lifespan_count=10,
            parameters=parameters
        )


query_params_1 = {"contexts": [context_1]}
language_code = 'en'
project_id=GOOGLE_PROJECT_ID
query_params=query_params_1
user_input=input_value
response = detect_intent_knowledge(
            project_id=GOOGLE_PROJECT_ID,
            session_id=session_id,
            # query_params=query_params_1,
            language_code=language_code,
            knowledge_base_id='NjY2OTEzNzgwNjA1NDM5MTgwOA',
            texts=['What are the things that you can do for me',]
            )

# def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):

