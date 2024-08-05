from scripts.Conversation import Conversation

from message_history import Message, MessageHistory

from typing import Dict, List, Any


class IntroConversation(Conversation):

    def __init__(
        self, model: Any, args: Dict, history: MessageHistory, context_length=10
    ):

        super().__init__(model, args, history, context_length=context_length)

        self.goals = [
            "Properly greet the user before starting the session",
        ]
        self.probe_questions = [
            "Has the user been greeted?",
        ]
        self.satisfied = [False] * len(self.probe_questions)
        self.goals_met = all(self.satisfied)

    def __str__(self):
        return "IntroConversation"
