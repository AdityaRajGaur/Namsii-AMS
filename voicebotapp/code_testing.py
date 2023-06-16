import openai


openai.api_key = "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"


def check_if_all_details_are_present(text):

    print("Check if details are received")

    prompt = "Check if all 2 ticket details are given by user for Application name and Description from:\n\nText: " + \
        text + "\n\nIn this format: Return 'True' if all details are given else 'False'"

    response = openai.Completion.create(

        engine="text-davinci-003",

        prompt=prompt,

        max_tokens=250,

        temperature=0.7,

        top_p=1.0,

        frequency_penalty=0.0,

        presence_penalty=0.0

    )

    print(response)

    if response.choices:

        true_or_false = response.choices[0].text.strip()

        print(type(true_or_false))

        print('response from check all details:', true_or_false)

        return true_or_false

    else:

        # API call failed or no data received

        print('Error: No response received from OpenAI API')


# text = "Create a ticket"

# check_if_all_details_are_present(text)
