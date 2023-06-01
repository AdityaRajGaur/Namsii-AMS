import openai




#openai.api_key = "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"

#openai.api_key = "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"

openai.api_key = "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"



def open_api_call():            #text- to be passed as input after testing

    text = "Create a jira ticket with high priority for Ecova project. I am not able to do order bookings, it says dates are already booked, selected items not available. Contact your application administrator"

     # Define the prompt for ticket details extraction

    prompt = "Extract ticket summary and description from:\n\nText: " + text + "\n\nSummary:\n\nDescription:\n\nProject Name:"




    response = openai.Completion.create(

        engine="text-davinci-003",

        prompt=prompt,

        max_tokens=2000,

        temperature=0.3,

        top_p=1.0,

        frequency_penalty=0.0,

        presence_penalty=0.0

    )




    if response.choices:

        summary = response.choices[0].text.strip()

        print('response from open ai call:',summary)





        # Split the string by newlines

        lines = summary.split('\n')

        print(lines)

    else:

        # API call failed or no data received

         print('Error: No response received from OpenAI API')





   

    project = ''

    summary_extract = ''

    priority = ''

    description = ''




    for line in lines:

        if line.startswith('Project:'):

            project = line.replace('Project:', '').strip()

        elif line.startswith('Summary:'):

            summary_extract = line.replace('Summary:', '').strip()

        elif line.startswith('Priority:'):

            priority = line.replace('Priority:', '').strip()

        # elif line.startswith('Description:'):

        #     description = line.replace('Description: \n', '').strip()

       

        # Iterate through the lines

    for i in range(len(lines)):

        if lines[i].startswith('Description:'):

            # Capture the subsequent lines until the next keyword or an empty line

            j = i + 1

            while j < len(lines) and not lines[j].startswith('Priority:') and lines[j].strip() != '':

                description += lines[j] + '\n'

                j += 1

            break




    # Remove leading/trailing whitespace from the description

        description = description.strip()




    print('Project:', project)

    print('Summary:', summary_extract)

    print('Priority:', priority)

    print('Description:', description)




    # return project,summary_extract,description



open_api_call()