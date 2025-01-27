import json
from time import sleep

from src.llm_client.azure_client import AzureClient
from src.function_calling.shopping import ShoppingBot


def shopping_action(item: str):
    """Invoke the shopping tool to simulate purchasing the item."""
    shopping = ShoppingBot()
    shopping.shopping(item)


class ShoppingAgent:
    def __init__(self):
        # Initialize the client and set up tools
        self.client = AzureClient().client
        self.tools = [{
            "type": "function",
            "function": {
                "name": "shopping",
                "description": "This function simulates a shopping action, where the user specifies an item they wish to purchase. The `item` parameter should be the name of the good being bought.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item": {
                            "type": "string",
                            "description": "The name of the item or goods to be purchased."
                        }
                    },
                    "required": ["item"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }]

    def process_user_request(self, query: str):
        """Process the user's request to purchase an item."""
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": query}],
            tools=self.tools
        )

        # Extract the tool call from the response
        tool_call = completion.choices[0].message.tool_calls[0]

        # Parse arguments from the tool call
        args = json.loads(tool_call.function.arguments)

        # Call the shopping function with the extracted item
        shopping_action(args["item"])

def shopping(user_input: str):
    shopping_agent = ShoppingAgent()

    shopping_agent.process_user_request(user_input)
    return "完成购物"

# Example usage of the agent
if __name__ == "__main__":

    agent = ShoppingAgent()

    user_input = input("对话开始:\n ")

    agent.process_user_request(user_input)

    sleep(10)
