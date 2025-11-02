from openai import OpenAI
import datetime
import json
import os
from classes.TextFileReader import TextFileReader

class OpenRouterClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPEN_ROUTER_API_KEY"),
                )
        self.completion = None

    def chat_mode(self, model, message = ""):
        print ("Hi")
        self.completion = self.client.chat.completions.create(
            extra_headers={
                # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },

            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }

            ],
            extra_body={
                "reasoning": {
                    "effort": "low",
                    "exclude": True
                }
            },
        )
        return self.completion.choices[0].message.content
    def get_response(self, promt, model="moonshotai/kimi-dev-72b:free"):
        # payload = json.dumps({
        #     "model": model,
        #     "messages": [
        #         {
        #             "role": "user",
        #             "content": promt
        #         }
        #     ],
        #     "temperature": temperature
        # })
        # response = requests.request("POST", self.url, headers=self.headers, data=payload)
        # return response.text

        self.completion = self.client.chat.completions.create(
            extra_headers={
                # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            extra_body={},
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": promt
                }
            ]
        )
        return self.completion.choices[0].message.content
