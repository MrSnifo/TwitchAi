"""
The MIT License (MIT)

Copyright (c) 2024-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from langchain_ollama import ChatOllama

__all__ = ('AI',)

class AI:
    def __init__(self, model: str):
        self.model = ChatOllama(model=model)
        self.system: str = (
            'You are a Twitch bot that responds to specific events with engaging, concise, and fun messages. '
            'When given an input message, rephrase or enhance it with random variations while keeping the meaning intact. '
            'If the message includes a user\'s name, always mention the name with an @ prefix '
            'Your responses must be Twitch-friendly, no longer than 500 characters, and entertaining. '
            'Do not discuss the bot, its limitations, or how it works.'
        )

    async def invoker(self, message):
        messages = [
            ('system', self.system),
            ('human', message),
        ]
        return await self.model.ainvoke(messages)