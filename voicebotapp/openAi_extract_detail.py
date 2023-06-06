import openai

openai.api_key = "insert api key here"


def open_api_call(text):            

    prompt = "Extract ticket details of project name,summary and description from:\n\nText: " + text + "\n\nIn this format: Project:\n\nSummary:\n\nDescription:\n\nProject Name:"

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
        elif line.startswith('Description:'):
             description = line.replace('Description: \n', '').strip()
        

    print('Project:', project)
    print('Summary:', summary_extract)
    print('Priority:', priority)
    print('Description:', description)

    return project,summary_extract,description



