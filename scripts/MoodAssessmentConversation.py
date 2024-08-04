from conversation import Conversation
from message_history import Message, MessageHistory
from typing import Dict, Any

class MoodAssessmentConversation(Conversation):

    def __init__(
        self, model: Any, args: Dict, history: MessageHistory, context_length=10
    ):
        super().__init__(model, args, history, context_length=context_length)
        self.goals = ["Assess the current mood of the user","Describe the mood of the user","Categorize the mood of the user"]
        self.probe_questions = ["What is the current state of users mood?", "Can you describe your mood?",
                                 "can you categorize your mood as positive, negative or neutral?"]
        self.satisfied = [False] * len(self.probe_questions)
        self.goals_met = all(self.satisfied)

    def __str__(self):
        return "MoodAssessmentConversation"
