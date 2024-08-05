import sys
sys.path.append('.')

from groq import Groq
from scripts.conversations import (
    ClosingConversation,
    EmotionalExplorationConversation,
    FeedbackConversation,
    MoodAssessmentConversation,
    PositiveReframingConversation,
    ProblemSolvingConversation,
    IntroConversation,
)

from ai71_model import AI71Model
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
            FeedbackConversation(model=self.model, args=self.args, history=self.history),
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
                rewritten_query: str = self.conversations[
                    self.current_conversation
                ].rewrite_query(user_query)

                self.history.add(Message(rewritten_query, "user"))

                ai_response: str = self.conversations[
                    self.current_conversation
                ].submit_query(rewritten_query)

                self.history.remove_last()
                self.history.add(Message(user_query, "user"))
                response = self.clear_clutter(ai_response)
                self.history.add(Message(response.content, "assistant"))
                print(f"HERE: {response}")
                return response
            
        return self.conclude_script()
    
    def clear_clutter(self, ai_response) -> Message:
        ai_response.content.replace("User:","")
        ai_response.content.replace("assistant:","")
        return ai_response

    def conclude_script(self) -> Message:
        # TODO
        return Message("Goodbye", "assistant")

    def goal_check(self):

        if self.conversations[self.current_conversation].has_met_goals():
            if str(self.conversations[self.current_conversation]).lower() == "feedbackconversation" :
                self.current_conversation = 1
            else :
                self.current_conversation += 1
        


if __name__ == "__main__":



    history_session = MessageHistory()
    therapy = TherapyScript(model= AI71Model(), args={}, history=history_session)
    while True:
        user_query = input("Human: ")
        if user_query.lower() == "exit":
            print("Ending Chat...")
            break
        elif user_query.lower() == "stat":
            history_session.get_statistics()
        elif user_query.lower() == "rst":
            history_session.clear()
        elif user_query.lower() == "show":
            history_session.show_history()
            print("\n")
        elif user_query.lower() == "curconv":
            current_converstion_index = therapy.current_conversation
            curr_conv = therapy.conversations[current_converstion_index]
            print(f"{current_converstion_index}-> {curr_conv}| satisfied : {curr_conv.satisfied} | has met goals : {curr_conv.goals_met}")
        else:
            response = therapy.submit_query(user_query)
            print(f"Therapist: {response.content}")
