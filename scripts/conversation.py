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

    def __str__(self):
        return "BaseConversation"

    def has_met_goals(self):
        if self.goals_met:
            return True
        goal_threads = []

        for i in range(len(self.probe_questions)):
            p = self.probe_questions[i]

            prompt = "Given the conversation history, answer 'yes' or 'no' "
            prompt += "to the following question with no elaboration or punctuation.\n"
            prompt += f"{p}\n"

            goal_threads.append(
                GoalThread(
                    messages=self.history.get_messages(self.context_length),
                    prompt=prompt,
                    model=self.model,
                )
            )
            for thread in goal_threads:
                thread.start()
            for thread in goal_threads:
                thread.join()
            for i, thread in enumerate(goal_threads):
                self.satisfied[i] = goal_threads[i].result.value.lower == "yes"
            self.goals_met = all(self.satisfied)
            return self.goals_met

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
