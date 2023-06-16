import openai


openai.api_key = "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"


def open_api_call(text):

    prompt = "Extract ticket details of application name, description, summary, and priority from:\nText: " + \
        text + "In this format: Application:\nDescription:\nSummary:\nPriority:"

    response = openai.Completion.create(

        engine="text-davinci-003",

        prompt=prompt,

        max_tokens=2000,

        temperature=0.3,

        top_p=1.0,

        frequency_penalty=0.0,

        presence_penalty=0.0

    )

    print(response)

    if response.choices:

        details = response.choices[0].text.strip()

        print('Response from OpenAI:', details)

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

            elif line.startswith('Description:'):

                description = line.replace('Description:', '').strip()

            elif line.startswith('Summary:'):

                summary = line.replace('Summary:', '').strip()

            elif line.startswith('Priority:'):

                priority = line.replace('Priority:', '').strip()

        print('Application:', application)

        print('Description:', description)

        print('Summary:', summary)

        print('Priority:', priority)

    else:

        print('Error: No response received from OpenAI API')


# old =proj,sum,des

# new = app_name,sum,des,priority

    return application, description, summary, priority
