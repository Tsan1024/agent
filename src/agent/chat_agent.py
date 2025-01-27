import time

from src.agent.prompt_template import prompt_template
from src.llm_client.azure_client import AzureClient



class ChatAgent:
    def __init__(self):
        # Initialize the client and set up tools
        self.client = AzureClient().client

    def process_user_request(self, query: str):
        """Process the user's request to purchase an item."""
        formatted_prompt = prompt_template.format(user_query=query)

        message = ""
        stream = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": formatted_prompt}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                message += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")
        return message

# Example usage of the agent
if __name__ == "__main__":
    agent = ChatAgent()
    user_input = input("对话开始:\n ")


    context = agent.process_user_request(user_input)

    # for chunk in agent.process_user_request(user_input):
    #     print(chunk, end=' ', flush=True)
    #     context = context + chunk
    print(context)