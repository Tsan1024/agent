# azureclient.py
import os
from openai import AzureOpenAI

# 设置环境变量
os.environ["GPT_API_KEY"] = "zzz"
os.environ["AZURE_OPENAI_ENDPOINT"] = "xxx"

class AzureClient:
    def __init__(self):
        """Initialize the client with Azure OpenAI API credentials."""
        self.client = AzureOpenAI(
            api_key=os.getenv("GPT_API_KEY"),
            api_version="2023-03-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def call_azure_openai(self, messages):
        """Call the Azure OpenAI API with the provided messages."""
        chat_completion = self.client.chat.completions.create(
            model="gpt-4o",  # Model deployment name
            messages=messages
        )
        return chat_completion.choices[0].message.content
