import sys
sys.path.append('.')
from ai71_model import AI71Model
from IntroConversation import IntroConversation
from message_history import Message, MessageHistory

from typing import Dict, List, Any

class TherapyScript:

    def __init__(self, model: Any, args: Dict, history: MessageHistory):
        self.history = history
        self.args = args
        self.model = model
        self.context_length = 10

        self.current_conversation = 0
        self.conversations = []
        self.conversations.append(
            IntroConversation(model=self.model, args=self.args, history=self.history)
        )

    def __str__(self):
        return "TalkerScript"

    def submit_query(self, user_query: str):
        if self.current_conversation < len(self.conversations):
            self.history.add(Message("user", user_query))
            self.goal_check()
            self.history.remove_last()
            if self.current_conversation < len(self.conversations):
                rewritten_query = self.conversations[
                    self.current_conversation
                ].rewrite_query(user_query)

                self.history.add(Message("user", rewritten_query))

                ai_response = self.conversations[
                    self.current_conversation
                ].submit_query(rewritten_query)

                return ai_response

    def goal_check(self):
        if self.conversations[self.current_conversation].has_met_goals():
            self.current_conversation += 1

if __name__ == "__main__":
    therapy = TherapyScript(model= AI71Model(), args={}, history=MessageHistory())
    a = therapy.submit_query("Hello")
    print(a.content)