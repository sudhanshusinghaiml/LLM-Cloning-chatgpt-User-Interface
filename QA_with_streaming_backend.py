""" This module contains the langchain integration with chainlit for developing a conversational application to  """

import chainlit as cl
import openai
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv

# Checking if the .env is loaded or not - Returns True
_ = load_dotenv(find_dotenv())

client = OpenAI()

# Setting the Environment Variables
client.api_key  = os.getenv('openai_api_key')

custom_template = \
"""Question: {question}
Answer: Let us think step by step."""

@cl.on_chat_start
def start_answering_prompt():
    prompt_template = PromptTemplate(
        template = custom_template,
        input_variables = ["question"]
    )

    llm_chain = LLMChain(llm=OpenAI(temperature=0.5, streaming=True),verbose=True
                         , prompt= prompt_template)

    cl.user_session.set("llm_chain", llm_chain)



@cl.on_message
async def handle_message_main(message: cl.Message):
    print(f"Received message: {message.content}")

    llm_chain = cl.user_session.get("llm_chain")

    # Prepare the input as a dictionary
    input_message = {"question": message.content}

    result = await llm_chain.acall(input_message, callbacks = [cl.AsyncLangchainCallbackHandler()])
    
    print(result)

    await cl.Message(content=result["text"]).send()