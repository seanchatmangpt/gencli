from fgn.completion.chat import achat

STATES = {"perceive": 0, "analyze": 1, "plan": 2, "act": 3, "learn": 4, "report": 5}

PROMPTS = {
    "perceive": "perception_prompt",
    "analyze": "analysis_prompt",
    "plan": "planning_prompt",
    "act": "action_prompt",
    "learn": "learning_prompt",
    "report": "reporting_prompt",
}


class Agent:
    def __init__(self, sys_msg, **kwargs):
        """Agent initializes itself."""
        self.__dict__.update(kwargs)
        self.sys_msg = sys_msg
        self.tasks = [
            self.perceive,
            self.analyze,
            self.plan,
            self.act,
            self.learn,
            self.report,
        ]
        self.state = None
        self.chat_log = []

    def __next__(self):
        """Agent performs a task."""
        for task in self.tasks:
            yield task()

    def __iter__(self):
        """Agent iterates over its tasks."""
        return self

    async def chat(self, prompt):
        """Agent chats with the environment."""
        result = await achat(prompt=prompt)
        self.chat_log.append({"state": self.state, "prompt": prompt, "result": result})
        return "chat", result

    async def act(self, prompt=PROMPTS["act"]):
        """Agent acts on the environment."""
        result = await self.chat(prompt=prompt)
        self.state = STATES["act"]
        return "act", result

    async def plan(self, prompt=PROMPTS["plan"]):
        """Agent plans for the future."""
        result = await self.chat(prompt=prompt)
        self.state = STATES["plan"]
        return "plan", result

    async def analyze(self, prompt=PROMPTS["analyze"]):
        """Agent analyzes the environment."""
        result = await self.chat(prompt=prompt)
        self.state = STATES["analyze"]
        return "analyze", result

    async def perceive(self, prompt=PROMPTS["perceive"]):
        """Agent perceives the environment."""
        result = await self.chat(prompt=prompt)
        self.state = STATES["perceive"]
        return "perceive", result

    async def learn(self, prompt=PROMPTS["learn"]):
        """Agent learns from the environment."""
        result = await self.chat(prompt=prompt)
        self.state = STATES["learn"]
        return "learn", result

    async def report(self, prompt=PROMPTS["report"]):
        """Agent reports its state."""
        result = await self.chat(prompt=prompt)
        self.state = STATES["report"]
        return "report", result
