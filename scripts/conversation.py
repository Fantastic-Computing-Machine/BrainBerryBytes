from re import M

from message_history import Message
from .reference import GoalThread


class Conversation:
    def __init__(self, model, args, history, context_length=10):
        self.history = history
        self.args = args
        self.model = model
        self.context_length = context_length

        self.goals = []
        self.probe_questions = []
        self.satisfied = [False] * len(self.probe_questions)
        self.goals_met = all(self.satisfied)

    def has_met_goals(self):
        if self.goals_met:
            return True
        goal_threads = []

        for i, p in enumerate(self.probe_questions):
            goal_threads.append(self._goal_check(p))

        for i, thread in enumerate(goal_threads):
            self.satisfied[i] = thread.result.value.lower == "yes"
        self.goals_met = all(self.satisfied)
        return self.goals_met

    def _goal_check(self, probe_question):
        prompt = "Given the conversation history, answer 'yes' or 'no' "
        prompt += "to the following question with no elaboration or punctuation.\n"
        prompt += f"{probe_question}\n"

        response = self.model.chat(prompt, self.history)
        return response

    def rewrite_query(self, query: str):
        return query

    def submit_query(self, query: str) -> Message:
        prompt = self._system_prompt()
        response = self.model.chat(query, self.history, prompt)
        message = Message(role="assistant", content=response)
        self.history.add_message(message)
        return message

    def _system_prompt(self):
        return "You are a helpful assistant."
