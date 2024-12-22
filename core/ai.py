from langchain_ollama import ChatOllama


class AI:

    def __init__(self, model: str):
        self.model = ChatOllama(model=model)
        self.system: str = (
            "You are a Twitch bot that responds to specific events with engaging, concise, and fun messages. "
            "When given an input message, rephrase or enhance it with random variations while keeping the meaning intact. "
            "If the message includes a user's name, always mention the name with an @ prefix "
            "Your responses must be Twitch-friendly, no longer than 500 characters, and entertaining. "
            "Do not discuss the bot, its limitations, or how it works."
        )

    async def invoker(self, message):
        messages = [
            ("system", self.system),
            ("human", message),
        ]
        return await self.model.ainvoke(messages)