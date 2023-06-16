import openai

openai.api_key = ""


def check_input(text):            

    prompt = "Check if user has given any ticket details from:\n\nText: " + text + "\n\nIn this format: Return 'True' if user input seems like he wants to create a ticket else return 'False'"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    #print("response:",response)
    if response.choices:
        flag = response.choices[0].text.strip()
        print('response from open ai call:',flag)

    else:
        # API call failed or no data received
         print('Error: No response received from OpenAI API')





