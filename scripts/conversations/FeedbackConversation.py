from scripts.Conversation import Conversation
from message_history import Message, MessageHistory
from typing import Dict, Any


class FeedbackConversation(Conversation):

    def __init__(
        self, model: Any, args: Dict, history: MessageHistory, context_length=10
    ):
        super().__init__(model, args, history, context_length=context_length)
        self.goals = [
            "Gather feedback from the user, if they have anything else to share.",
            "Assess user satisfaction with the conversation"
        ]
        self.probe_questions = [
            "Has the user have any thing else to share?"
            "Has the user not satisfied with the conversation?",
        ]
        self.satisfied = [False] * len(self.probe_questions)
        self.goals_met = all(self.satisfied)

    def __str__(self):
        return "FeedbackConversation"
