import chainlit as cl
from openai import OpenAI

# Use the below codes to load the passowrd in py or ipynb files
import os
from dotenv import load_dotenv, find_dotenv


# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())

client = OpenAI()

# Setting the Environment Variables
client.api_key  = os.getenv('openai_api_key')

def get_openaigpt_output(user_message):
    response = client.chat.completions.create(
        model= 'gpt-4',
        messages= [
            {
                "role": "system",
                "content": "you are an assistant that is obsessed with Cricket facts and figures"
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature= 1,
        max_tokens= 256,
        top_p= 1,
        frequency_penalty= 0,
        presence_penalty= 0
    )

    print(response.choices[0].message.content)

    return response.choices[0].message.content


@cl.on_message
async def main(message):
    # Get the response from GPT-4 and send it as a Chainlit message
    await cl.Message(content = get_openaigpt_output(message.content)).send()
