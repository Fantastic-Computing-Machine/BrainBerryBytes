import os
from message_history import MessageHistory, Message
from typing import Optional, List
from openai import OpenAI

MODELS = ["tiiuae/falcon-11b", "tiiuae/falcon-180b-chat"]

API_KEY = "ai71-api-437ee0ac-2734-4d99-8730-0482e57edd13"
BASE_URL = "https://api.ai71.ai/v1/"


class AI71Model:

    def __init__(
        self,
        api_key: str = ...,
        model: str = MODELS[1],
        temperature: float = 0.7,
        args: dict = {},
    ):
        self.api_key = api_key
        self.model = model
        self.temperature: float = temperature
        self.args = args
        self.ai71_client = self.get_client()

        # User attrs
        self.full_name = args.get("full_name", "User")
        self.mood_state: list = args.get("mood_state", [])

    def get_client(self):
        return OpenAI(api_key=self.api_key, base_url=BASE_URL)

    def chat(
        self,
        history: MessageHistory = MessageHistory(),
        args: dict = {},
        system_prompt: Optional[str] = None,
    ) -> Message:

        if not system_prompt:
            system_prompt = self.system_prompt()

        messages = self.rewrite_history(history=history, system_prompt=system_prompt)
        response = self.ai71_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        return Message(response.choices[0].message.content, "assistant")

    def rewrite_query(self, query: str):
        # TODO: Write Prompt
        return query

    def system_prompt(self) -> str:
        # TODO: Write Prompt
        q = "You are a helpful Therapist who is here to listen to the user."
        q += "You can ask the user about their mood, and offer support."
        q += "You can also ask the user about their day, and offer advice."
        q += "your goal is to analyze the user's mood and provide support."
        return q

    def rewrite_history(
        self, history: MessageHistory, system_prompt: str
    ) -> List[dict]:

        formatted_history = []
        for message in history.get_messages():
            formatted_history.append(message.passable)

        if system_prompt:
            formatted_history.append({"role": "system", "content": system_prompt})
        else:
            formatted_history.append(
                {"role": "system", "content": self.system_prompt()}
            )

        return formatted_history

    def make_message(self, message: Message) -> dict:
        return {"role": message.role, "content": message.content}


if __name__ == "__main__":
    history = MessageHistory()
    ai71 = AI71Model()

    while True:
        user_query = input("User -> ")
        history.add(Message(user_query, "user"))
        response = ai71.chat(history)
        print("AI -> ", response.content)
        history.add(response)
        print(history.get_statistics())
