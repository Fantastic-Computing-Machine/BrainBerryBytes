from typing import List


class Message:

    def __init__(self, content: str, role: str):
        self.role = role
        self.content = content

    def __str__(self):
        return f"\t\t{self.role}: {self.content}"

    @property
    def passable(self) -> dict:
        return {"role": self.role, "content": self.content}


class MessageHistory:

    def __init__(self, messages: List[Message] = []):
        self.history = []
        if messages:
            self.history += messages

    def add(self, message: Message):
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

    def get_statistics(self):
        """
        Get statistics of the conversation
        """
        stats = {"user": 0, "assistant": 0, "system": 0}
        for message in self.history:
            if message.role in stats:
                stats[message.role] += 1
        print(
            f"\nUser: {stats['user']}\nAssistant: {stats['assistant']}\nSystem: {stats['system']}\n"
        )

    def show_history(self):
        print("*" * 20)
        for message in self.history:
            print(message)
        print("*" * 20)
