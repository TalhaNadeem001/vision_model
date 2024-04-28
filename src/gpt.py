import os
import openai
import asyncio
from src.config_example import gpt_key

sys_content = ( "Your name is sage"
    "I want you to act like a voice assistant, keep your responses short and simple, if longer responses are required then do so"
               "Note that if you cannot answer the question which is about "
                   "something you do not know such as time-sensitive information(e.g. "
                   "today's weather/stock, .etc), you can only reply \"IDK\" in your response without other characters."
                   "Do not say something like As an AI language model..., I'm sorry... and etc."
                   "Whenever possible always add a suggestion at the end of your response")

class ChatGPT:
    def __init__(self):
        openai.api_key = gpt_key
        self.messages = [
            {"role": "system", "content": sys_content},
        ]

    async def gpt(self, prompt, lang):
        if prompt is None:
            return
        prompt += "\n"
        self.messages.append({"role": "user", "content": prompt})
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=self.messages
        )
        self.messages.append({"role":"assistant", "content": response['choices'][0]['message']["content"]})
        return response
