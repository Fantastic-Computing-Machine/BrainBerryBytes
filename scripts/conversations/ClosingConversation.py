from scripts.Conversation import Conversation
from message_history import Message, MessageHistory
from typing import Dict, Any


class ClosingConversation(Conversation):

    def __init__(
        self, model: Any, args: Dict, history: MessageHistory, context_length=10
    ):
        super().__init__(model, args, history, context_length=context_length)
        self.goals = [
            "Closing the conversation",
            "Ensuring the user is satisfied",
            "Ensuring the user is ready to end the conversation",
        ]
        self.probe_questions = [
            "Has the user expressed that they are ready to end the conversation?",
            "Has the user said goodbye?",
            "Has the user expressed that they are satisfied with the conversation?",
        ]
        self.satisfied = [False] * len(self.probe_questions)
        self.goals_met = all(self.satisfied)

    def __str__(self):
        return "ClosingConversation"
