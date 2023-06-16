#Curie model tested here,found inefficient for the required purpose

import openai
import os
import requests
import json

openai.api_key = ""
openai.api_base = "https://voicebotwest.openai.azure.com/"
openai.api_type = 'azure'
deployment_name='my-curie-model'
openai.api_version = "2022-12-01"



def open_api_call(prompt):            
    print("func called")

#"curie.ft-7bc1b92426fa4f999d31cf7be24544ec-Test"

    response = openai.ChatCompletion.create(
        engine=deployment_name,
        prompt=prompt,
        max_tokens=50,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print(response.choices[0].text)
    if response.choices:
        completion = response.choices[0].text.strip()
        print('api response: ',completion)
    else:
        print('Error: No response received from OpenAI API')


prompt = "i need to book a flight ticket"
open_api_call(prompt)


