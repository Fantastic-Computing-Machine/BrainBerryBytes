from typing import List


class Message:
    def __init__(self, content: str, role):
        self.role = role
        self.content = content


class MessageHistory:

    def __init__(self, messages: List[Message] = []):
        self.history = []
        if messages:
            self.history += messages

    def add_message(self, message: Message):
        self.history.append(message)

    def get_messages(self, count: int = -1):
        if count >= 0:
            return self.history[-count:]
        return self.history

    def clear(self):
        self.history = []

    def remove_last(self):
        self.history.pop()

    def __len__(self):
        return len(self.history)

    def load_messages(self, args):
        """
        Load messages from database
        """
        pass
