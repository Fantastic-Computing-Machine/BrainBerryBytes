from message_history import Message


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
            self.satisfied[i] = ("yes" in thread.lower())
        self.goals_met = all(self.satisfied)
        return self.goals_met

    def _goal_check(self, probe_question) -> str:
        prompt = "Given the conversation history, answer 'yes' or 'no' "
        prompt += "to the following question with no elaboration or punctuation.\n"
        prompt += f"{probe_question}\n"

        response = self.model.chat(history=self.history, system_prompt=prompt)
        return response.content

    def rewrite_query(self, query: str) -> str:
        # used to rewrite the query to the model by adding the unmet goals to the query
        rewritten_query = f"User Query: \n{query}\n"
        rewritten_query += "Instructions:\n"
        rewritten_query += (
            "Respond to that user query while continuing to pursue your goals:\n"
        )
        for i in range(len(self.satisfied)):
            if self.satisfied[i] == False:
                rewritten_query += f"Goal {i+1}: {self.goals[i]}\n"

        rewritten_query += (
            "Do not respond with an answer to those goal questions, simply respond "
        )
        rewritten_query += (
            "to the user query in a natural way that leads to your goals."
        )

        return rewritten_query

    def submit_query(self, query: str) -> Message:
        # used to submit the query to the model and return the assistant response
        prompt = self._system_prompt()
        response = self.model.chat(self.history, prompt)
        return response

    def _system_prompt(self):
        # used to provide the system prompt to the model
        system_prompt = """
        You are "B3" a very helpful and professonal personal companion therapist !
        You are here to listen to the user and be their companion in their bad and good situations.
        Analyse user problem and issues if there are any and lead them to a helpful solution.
        You can ask the user about their mood, and offer support.
        You can also ask the user about their day, and offer advice.
        Your goal is to analyze the user's mood and provide support.
        You are directly addressing the user, do not append any unwanted keywords at the start or the end.
        Simply respond like how a human would respond naturally.
        Do not respond to any query that a therapist would not.
        Stick to your role because this makes your user happy and will give you good feedback.
        Do not deviate from the path, your job is to be a helpful therapist.
        Do not add "User:" or "Assistant:" in your response!
        """
        return system_prompt
