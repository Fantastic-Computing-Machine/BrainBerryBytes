import os
from ai71 import AI71
from message_history import MessageHistory, Message
from typing import Optional, List
from openai import OpenAI

MODELS = ["tiiuae/falcon-11b", "tiiuae/falcon-180b-chat"]

API_KEY = os.getenv("AI71_API_KEY")
BASE_URL = "https://api.ai71.ai/v1/"


class AI71Model:

    def __init__(
        self,
        model: str = "tiiuae/falcon-11b",
        temperature: float = 0.4,
        args: dict = {},
    ):
        self.model = model
        self.temperature: float = temperature
        self.args = args

        self.ai71_client = self.get_client()

        # User attrs
        self.full_name = args.get("full_name", "User")
        self.mood_state: list = args.get("mood_state", [])

    def get_client(self):
        return OpenAI(api_key=API_KEY, base_url=BASE_URL)

    def chat(self, query: str, history: MessageHistory = MessageHistory()):

        rewritten_query = self.rewrite_query(query)

        if history:
            messages = self.rewrite_history(history, rewritten_query)

        response = self.ai71_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query},
            ],
            temperature=self.temperature,
        )

        print(response)

        return response.choices[0].message

    def rewrite_query(self, query: str):
        return query

    def system_prompt(self): ...

    def rewrite_history(self, history: MessageHistory, query: str) -> List[dict]:

        return [{}]


if __name__ == "__main__":
    ai71 = AI71Model()
    print(ai71.chat("Hello"))
