from .IntroConversation import IntroConversation


class TherapyScript:
    def __init__(self, model, args, history):
        self.history = history
        self.args = args
        self.model = model

        self.current_conversation = 0
        self.conversations = [
            IntroConversation,
        ]
        self.context_length = 10

    def __str__(self):
        return "TalkerScript"

    def submit_query(self): ...

    def goal_check(self):

        pass
