import openai

openai.api_key = ""


def open_api_call(text):            
    prompt = "Extract application name, severity and very detailed description, short summary from:\nText: " + text + "In this format: Application:\n Description:\n Summary:\n Priority:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # print(response)
    if response.choices:
        details = response.choices[0].text.strip()
        print('\n\n\nResponse from OpenAI:')

        # Split the string by newlines
        lines = details.split('\n')

        # Initialize variables
        application = ''
        description = ''
        summary = ''
        priority = ''

        for line in lines:
            if line.startswith('Application:'):
                application = line.replace('Application:', '').strip()            
            elif line.startswith('Summary:'):
                summary = line.replace('Summary:', '').strip()
            elif line.startswith('Priority:'):
                priority = line.replace('Priority:', '').strip()
            elif line.startswith('Description:'):
                description = line.replace('Description:', '').strip() + ' This is for Application- '+ application    

        print('Application:', application)
        print('Description:', description )
        print('Summary:', summary)
        print('Priority:', priority)
    else:
        print('Error: No response received from OpenAI API')

    
    if  (priority).lower() in ['medium','medium.']:
        priority='Medium'        
    if  (priority).lower() in ['low','low.']:
        priority='Low'
    if  (priority).lower() in ['showstopper','show stopper','showstopper.']:
        priority='Showstopper'
    if  (priority).lower() in ['high','high.']:
        priority='High'     
    if  (priority).lower() in ['trivial','trivial.']:
        priority='Trivial' 
    print('Priority:', priority)
#old =proj,sum,des
#new = app_name,sum,des,priority
    return application,description,summary,priority


# open_api_call(' for "Leave Management" application with severity as Trivial.')    

#Input from Dialogflow - 

# I am not able to login in the VDI machine after yeterday shutdown. Tried calling helpdesk and send an email
# but did not receive any response. So not able to perform daily tasks for Application - Leave Management Portal
# and Severity - Showstopper