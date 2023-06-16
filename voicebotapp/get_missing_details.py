import openai

openai.api_key = "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"



def check_if_all_details_are_presents(text):            
    print("Check if details are received")
    prompt = "Check if Application name, Description and Priority are given clearly, and mention which is not given from:\n\nText: " + text+ "in this format: Application:True/False Description:True/False Priority:True/False"

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
        input_string = response.choices[0].text.strip()
        print('response from check all details:',input_string)

       # Split the input string by newline character and remove leading/trailing whitespace
        pairs = input_string.strip().split("\n")

        # Initialize lists to store true and false values
        true_values = []
        false_values = []

        # Iterate over each pair and extract the key and value
        for pair in pairs:
            key_value = pair.split(":")
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()

                # Check if the value is true or false and append to the corresponding list
                if value.lower() == "true":
                    true_values.append(key)
                elif value.lower() == "false":
                    false_values.append(key)

        # Create the output text with the false values
        output_text = "Please provide details of "
        missing_details = ", ".join(false_values)

        # Check the number of missing details and append them accordingly
        if len(false_values) > 1:
            output_text += missing_details.replace(", ", " and ")
        elif len(false_values) == 1:
            output_text += missing_details

        # Print the true values and the output text with the false values
        print("True values:", true_values)
        print("Output text:", output_text)
        if len(true_values) == 3:
            val= 1
        else:
            val = 0
            print("details missing")
        return val,output_text

    else:
        # API call failed or no data received
         print('Error: No response received from OpenAI API')


# text = "'Application: True\nDescription: True\nPriority: False'"
# check_if_all_details_are_presents(text)

    




