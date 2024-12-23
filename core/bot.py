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

from twitch.ext.oauth import DeviceAuthFlow, Scopes
from twitch.types import eventsub
from twitch import Client
from .utils import AI

import logging
_logger = logging.getLogger(__name__)


__all__ = ("TwitchBot",)


class TwitchBot(Client):
    def __init__(self, client_id: str, ai_model: str, cli: bool = False) -> None:
        super().__init__(client_id, cli=cli)
        # Set Up AI.
        self.ai: AI = AI(model=ai_model)

        # Set up OAuth authentication flow.
        self.auth_flow: DeviceAuthFlow = DeviceAuthFlow(
            self,
            scopes=[
                Scopes.USER_READ_CHAT,
                Scopes.BITS_READ,
                Scopes.MODERATOR_READ_FOLLOWERS,
                Scopes.CHANNEL_READ_SUBSCRIPTIONS,
                Scopes.CHANNEL_READ_POLLS,
                Scopes.CHANNEL_READ_PREDICTIONS,
                Scopes.CHANNEL_READ_HYPE_TRAIN,
                Scopes.MODERATOR_READ_SHOUTOUTS,
                Scopes.USER_WRITE_CHAT
            ],
            dispatch=False,
            wrap_run=False
        )

    async def send_message(self, content: str) -> None:
        """
        Send a message to the Twitch channel chat.
        """
        try:
            await self.channel.chat.send_message(content.strip('"'))
        except Exception as e:
            _logger.error(f"Failed to send message: {e}")

    async def on_ready(self) -> None:
        """
        Called when the bot is successfully connected and ready.
        """
        _logger.info("Bot is ready to be used.")

    async def on_chat_message(self, data: eventsub.chat.MessageEvent) -> None:
        """
        Respond to chat messages, specifically those starting with "!ask".
        """
        message = data['message']['text']
        if message.startswith("!ask"):
            query = f"{data['chatter_user_name']}: {message[5:].strip()}"
            response = await self.ai.invoker(query)
            await self.send_message(response.content)

    async def on_chat_clear(self, data: eventsub.chat.ChatClearEvent) -> None:
        """
        Handle chat clear events by generating a random joke or message.
        """
        response = await self.ai.invoker("Someone has cleared the chat. Make a joke or do something random.")
        await self.send_message(response.content)

    async def on_shared_chat_begin(self, data: eventsub.chat.SharedChatBeginEvent) -> None:
        """
        Handle shared chat beginning by notifying about the shared chat.
        """
        response = await self.ai.invoker(f"The chat is now shared with {data['broadcaster_user_name']}.")
        await self.send_message(response.content)

    async def on_shared_chat_end(self, data: eventsub.chat.SharedChatEndEvent) -> None:
        """
        Handle shared chat ending by notifying about the shared chat ending.
        """
        response = await self.ai.invoker(f"The chat is no longer shared with {data['broadcaster_user_name']}.")
        await self.send_message(response.content)

    async def on_cheer(self, data: eventsub.bits.CheerEvent) -> None:
        """
        Handle cheer events and notify about bits cheer.
        """
        user = "Someone" if data['is_anonymous'] else data['user_name']
        response = await self.ai.invoker(f"{user} has cheered {data['bits']} bits!")
        await self.send_message(response.content)

    async def on_follow(self, data: eventsub.channels.FollowEvent) -> None:
        """
        Handle follow events and notify about new followers.
        """
        response = await self.ai.invoker(f"{data['user_name']} has followed the channel!")
        await self.send_message(response.content)

    async def on_subscribe(self, data: eventsub.channels.SubscribeEvent) -> None:
        """
        Handle subscription events and notify about new subscriptions.
        """
        response = await self.ai.invoker(f"{data['user_name']} has subscribed to the channel!")
        await self.send_message(response.content)

    async def on_subscription_end(self, data: eventsub.channels.SubscriptionEndEvent) -> None:
        """
        Handle subscription expiration events and notify when a subscription ends.
        """
        response = await self.ai.invoker(f"{data['user_name']}'s subscription has expired.")
        await self.send_message(response.content)

    async def on_subscription_gift(self, data: eventsub.channels.SubscriptionGiftEvent) -> None:
        """
        Handle subscription gift events and notify about gifted subscriptions.
        """
        user = "Someone" if data['is_anonymous'] else data['user_name']
        response = await self.ai.invoker(f"{user} gifted {data['total']} subs at tier {data['tier']}!")
        await self.send_message(response.content)

    async def on_subscription_message(self, data: eventsub.channels.SubscriptionMessageEvent) -> None:
        """
        Handle subscription message events and notify about subscription messages.
        """
        response = await self.ai.invoker(f"{data['user_name']} resubscribed: {data['message']}")
        await self.send_message(response.content)

    async def on_poll_begin(self, data: eventsub.interaction.PollBeginEvent) -> None:
        """
        Handle poll start events and notify about the beginning of a poll.
        """
        response = await self.ai.invoker(f"A poll has started: {data['title']}")
        await self.send_message(response.content)

    async def on_poll_end(self, data: eventsub.interaction.PollEndEvent) -> None:
        """
        Handle poll end events and notify about the conclusion of a poll.
        """
        response = await self.ai.invoker(f"The poll has ended: {data['title']}")
        await self.send_message(response.content)

    async def on_prediction_begin(self, data: eventsub.interaction.PredictionBeginEvent) -> None:
        """
        Handle prediction start events and notify about the beginning of a prediction.
        """
        response = await self.ai.invoker(f"A prediction has started: {data['title']}")
        await self.send_message(response.content)

    async def on_prediction_end(self, data: eventsub.interaction.PredictionEndEvent) -> None:
        """
        Handle prediction end events and notify about the conclusion of a prediction.
        """
        response = await self.ai.invoker(f"The prediction has ended: {data['title']}")
        await self.send_message(response.content)

    async def on_hype_train_begin(self, data: eventsub.interaction.HypeTrainEvent) -> None:
        """
        Handle hype train start events and notify about the start of a hype train.
        """
        response = await self.ai.invoker("The hype train has started!")
        await self.send_message(response.content)

    async def on_hype_train_end(self, data: eventsub.interaction.HypeTrainEndEvent) -> None:
        """
        Handle hype train end events and notify about the end of a hype train.
        """
        response = await self.ai.invoker("The hype train has ended.")
        await self.send_message(response.content)

    async def on_raid(self, data: eventsub.streams.RaidEvent) -> None:
        """
        Handle raid events and notify about incoming raids.
        """
        response = await self.ai.invoker(f"{data['from_broadcaster_user_name']} has raided the channel with"
                                         f" {data['viewers']} viewers!")
        await self.send_message(response.content)

    async def run_bot(self) -> None:
        """
        Start the Twitch bot, authenticate, and begin listening for events.
        """
        # Start the authentication process
        async with self.auth_flow:
            user_code, device_code, expires_in, interval = await self.auth_flow.get_device_code()
            _logger.info('Authorization URL: https://www.twitch.tv/activate?device-code=%s', user_code)

            try:
                access_token, refresh_token = await self.auth_flow.poll_for_authorization(
                    device_code, expires_in, interval
                )
            except Exception as e:
                _logger.error(f'Failed to authorize: {e}')
                return

        # Start the bot with the obtained tokens
        async with self:
            await self.start(access_token, refresh_token)
