from re import M

from message_history import Message
from reference import GoalThread


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
        # used to rewrite the query to the model by adding the unmet goals to the query
        rewritten_query = f"User Query: \n{query}\n"
        rewritten_query += "Instructions:\n"
        rewritten_query += "Repeat the user query while continue to persue your goals.\n"
        for i in range(len(self.satisfied)):
            if self.satisfied[i] == False:
                rewritten_query += f"Goal: {self.goals[i]}\n"
        
        rewritten_query += "Don not provide any reposnse to the goal questions. \n"
        rewritten_query += "Only respond to the user query, in a natural way that lead to you goal \n"

        return rewritten_query

    def submit_query(self, query: str) -> Message:
        # used to submit the query to the model and return the assistant response
        prompt = self._system_prompt()
        response = self.model.chat(query, self.history, prompt)
        message = Message(role="assistant", content=response)
        self.history.add_message(message)
        return message

    def _system_prompt(self):
        # used to provide the system prompt to the model
        system_prompt = "You are a helpful Therapist who is here to listen to the user."
        system_prompt += "You can ask the user about their mood, and offer support."
        system_prompt += "You can also ask the user about their day, and offer advice."
        system_prompt += "your goal is to analyze the user's mood and provide support."
        return system_prompt
