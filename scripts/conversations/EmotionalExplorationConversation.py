from scripts.Conversation import Conversation
from message_history import Message, MessageHistory
from typing import Dict, Any


class EmotionalExplorationConversation(Conversation):

    def __init__(
        self, model: Any, args: Dict, history: MessageHistory, context_length=10
    ):
        super().__init__(model, args, history, context_length=context_length)
        self.goals = [
            "Understand why the user is feeling down or happy",
            "",
            "Identify triggers for the user's current mood",
        ]
        self.probe_questions = [
            "Has the user expressed why they are feeling down or happy?",
            "Has the user provided specific events or reasons for their emotions?",
        ]
        self.satisfied = [False] * len(self.probe_questions)
        self.goals_met = all(self.satisfied)

    def __str__(self):
        return "EmotionalExplorationConversation"
