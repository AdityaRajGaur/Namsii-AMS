import openai

openai.api_key = "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"


def random_query_handler(text):            

    prompt = "You are a voice bot technical support assistant,provide a response for Text: " + text

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=75,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print("From Random query handler:")
    return response.choices[0].text.strip()



