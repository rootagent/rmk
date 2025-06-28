from rmonkey.agents import Agent


class AskAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(name="AskAgent", system="You are a powerful AI agent.", **kwargs)
        self.description = "This agent is used to answer questions."
