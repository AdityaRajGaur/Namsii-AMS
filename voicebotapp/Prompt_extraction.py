#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
# openai.api_type = "azure"
# openai.api_base = "https://voicebotwest.openai.azure.com/"
# openai.api_version = "2023-03-15-preview"
# #openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = "9a62b3f0382a4fb496ef0e996630bbb9"
openai.api_type = "azure"
openai.api_base = "https://testazopenai.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = ""

#old system msg   As a support assistant,check if user intents to create a ticket for his technical problem if any or not based on input. If 'yes' then return only 'True' else return 'False', Just respond with True and False"
#function to check user intent
def openAIChatCompletion(prompt):

    response = openai.ChatCompletion.create(
    engine="TR",
    messages = [{"role":"system","content":"You are a voice bot assistant, return 'True' when user intents to create a ticket or a ticket should be created for his mentioned technical problem, else return 'False'"},\
                {"role":"user","content":"Facing issue with login to Azure"},{"role":"assistant","content":"True"},\
                {"role":"user","content":"My cat is lost"},{"role":"assistant","content":"False"},\
                {"role":"user","content":"Azure is down"},{"role":"assistant","content":"False"},\
                {"role":"user","content":"Server issue"},{"role":"assistant","content":"False"},\
                {"role":"user","content":"How is the weather"},{"role":"assistant","content":"False"},\
                {"role":"user","content":"my laptop is not working."},{"role":"assistant","content":"True"},\
                {"role":"user","content":"My water bottle is lost"},{"role":"assistant","content":"True"},\
                {"role":"user","content":"Create a ticket"},{"role":"assistant","content":"True"}],
    temperature=0.7,
    max_tokens=250,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)

    

    print("Output received: "+response['choices'][0]['message']['content'])


#testing prompts
prompt = "create a jira ticket"
#openAIChatCompletion(prompt)