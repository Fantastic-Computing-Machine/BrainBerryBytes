import sys
sys.path.append('.')
from scripts.ClosingConversation import ClosingConversation 
from scripts.EmotionalExplorationConversation import EmotionalExplorationConversation
from scripts.MoodAssessmentConversation import MoodAssessmentConversation
from scripts.PositiveReframingConversation import PositiveReframingConversation
from scripts.ProblemSolvingConversation import ProblemSolvingConversation
from ai71_model import AI71Model
from IntroConversation import IntroConversation
from message_history import Message, MessageHistory

from typing import Dict, List, Any, Optional

class TherapyScript:

    def __init__(self, model: Any, args: Dict, history: MessageHistory):
        self.history = history
        self.args = args
        self.model = model
        self.context_length = 10

        self.current_conversation = 0
        self.conversations = []
        self.conversations.extend([
            IntroConversation(model=self.model, args=self.args, history=self.history),
            MoodAssessmentConversation(model=self.model, args=self.args, history=self.history),
            EmotionalExplorationConversation(model=self.model, args=self.args, history=self.history),
            ProblemSolvingConversation(model=self.model, args=self.args, history=self.history),
            PositiveReframingConversation(model=self.model, args=self.args, history=self.history),
            ClosingConversation(model=self.model, args=self.args, history=self.history),]
        )

    def __str__(self):
        return "TalkerScript"

    def submit_query(self, user_query: str) -> Message:
        if self.current_conversation < len(self.conversations):
            print()
            self.history.add(Message(user_query, "user"))
            self.goal_check()
            self.history.remove_last()
            if self.current_conversation < len(self.conversations):
                rewritten_query = self.conversations[
                    self.current_conversation
                ].rewrite_query(user_query)

                self.history.add(Message(rewritten_query, "user"))

                ai_response = self.conversations[
                    self.current_conversation
                ].submit_query(rewritten_query)

                return ai_response
        return self.conclude_script()

    def conclude_script(self) -> Message:
        # TODO
        return Message("Goodbye", "assistant")

    def goal_check(self):
        if self.conversations[self.current_conversation].has_met_goals():
            self.current_conversation += 1


if __name__ == "__main__":
    history_session = MessageHistory()
    therapy = TherapyScript(model= AI71Model(), args={}, history=history_session)
    while True:
        user_query = input("Human: ")
        response = therapy.submit_query(user_query)
        history_session.add(response)
        print(f"Therapist: {response.content}")
