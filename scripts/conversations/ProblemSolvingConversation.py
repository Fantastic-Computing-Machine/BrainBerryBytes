from scripts.Conversation import Conversation
from message_history import Message, MessageHistory
from typing import Dict, Any


class ProblemSolvingConversation(Conversation):

    def __init__(
        self, model: Any, args: Dict, history: MessageHistory, context_length=10
    ):
        super().__init__(model, args, history, context_length=context_length)
        self.goals = [
            "Help the user with problem-solving strategies",
            "Guide the user to identify potential solutions",
        ]
        self.probe_questions = [
            "Has the user described their problem?",
            "Has the user identified potential solutions?",
        ]
        self.satisfied = [False] * len(self.probe_questions)
        self.goals_met = all(self.satisfied)

    def __str__(self):
        return "ProblemSolvingConversation"
