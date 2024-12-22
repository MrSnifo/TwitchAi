from sqlite3.dbapi2 import paramstyle
from typing import Optional

from twitch.types import eventsub
from twitch import Client
from .ai import AI
from twitch import setup_logging


from twitch.ext.oauth import DeviceAuthFlow, Scopes


class Twitch(Client):
    def __init__(self, client_id: str, ai_model: str):
        super().__init__(client_id, cli=True)

        self.ai: Optional[AI] = AI(model=ai_model)
        self.auth_flow: DeviceAuthFlow = DeviceAuthFlow(
            self,
            scopes=[Scopes.USER_READ_CHAT,
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

    async def send_message(self, content: str):
        try:
            await self.channel.chat.send_message(content.strip('"'))
        except Exception as e:
            print(f"Failed to send message: {e}")

    async def on_ready(self) -> None:
        print("Bot is ready to be used")

    async def on_chat_message(self, data: eventsub.chat.MessageEvent):
        message = data['message']['text']
        if message.startswith("!ask "):
            print("??")
            query = message[5:].strip()
            response = await self.ai.invoker(query)
            await self.send_message(response.content)

    async def on_chat_clear(self, data: eventsub.chat.ChatClearEvent):
        response = await self.ai.invoker("Someone has cleared the chat. Make a joke or do something random.")
        await self.send_message(response.content)

    async def on_shared_chat_begin(self, data: eventsub.chat.SharedChatBeginEvent):
        response = await self.ai.invoker(f"The chat is now shared with {data['broadcaster_user_name']}.")
        await self.send_message(response.content)

    async def on_shared_chat_end(self, data: eventsub.chat.SharedChatEndEvent):
        response = await self.ai.invoker(f"The chat is no longer shared with {data['broadcaster_user_name']}.")
        await self.send_message(response.content)

    async def on_cheer(self, data: eventsub.bits.CheerEvent):
        user = "Someone" if data['is_anonymous'] else data['user_name']
        response = await self.ai.invoker(f"{user} has cheered {data['bits']} bits!")
        await self.send_message(response.content)

    async def on_follow(self, data: eventsub.channels.FollowEvent):
        response = await self.ai.invoker(f"{data['user_name']} has followed the channel!")
        await self.send_message(response.content)

    async def on_subscribe(self, data: eventsub.channels.SubscribeEvent):
        response = await self.ai.invoker(f"{data['user_name']} has subscribed to the channel!")
        await self.send_message(response.content)

    async def on_subscription_end(self, data: eventsub.channels.SubscriptionEndEvent):
        response = await self.ai.invoker(f"{data['user_name']}'s subscription has expired.")
        await self.send_message(response.content)

    async def on_subscription_gift(self, data: eventsub.channels.SubscriptionGiftEvent):
        user = "Someone" if data['is_anonymous'] else data['user_name']
        response = await self.ai.invoker(f"{user} gifted {data['total']} subs at tier {data['tier']}!")
        await self.send_message(response.content)

    async def on_subscription_message(self, data: eventsub.channels.SubscriptionMessageEvent):
        response = await self.ai.invoker(f"{data['user_name']} resubscribed: {data['message']}")
        await self.send_message(response.content)

    async def on_poll_begin(self, data: eventsub.interaction.PollBeginEvent):
        response = await self.ai.invoker(f"A poll has started: {data['title']}")
        await self.send_message(response.content)

    async def on_poll_end(self, data: eventsub.interaction.PollEndEvent):
        response = await self.ai.invoker(f"The poll has ended: {data['title']}")
        await self.send_message(response.content)

    async def on_prediction_begin(self, data: eventsub.interaction.PredictionBeginEvent):
        response = await self.ai.invoker(f"A prediction has started: {data['title']}")
        await self.send_message(response.content)

    async def on_prediction_end(self, data: eventsub.interaction.PredictionEndEvent):
        response = await self.ai.invoker(f"The prediction has ended: {data['title']}")
        await self.send_message(response.content)

    async def on_hype_train_begin(self, data: eventsub.interaction.HypeTrainEvent):
        response = await self.ai.invoker("The hype train has started!")
        await self.send_message(response.content)

    async def on_hype_train_end(self, data: eventsub.interaction.HypeTrainEndEvent):
        response = await self.ai.invoker("The hype train has ended.")
        await self.send_message(response.content)

    async def on_raid(self, data: eventsub.streams.RaidEvent):
        response = await self.ai.invoker(f"{data['from_broadcaster_user_name']} has raided the channel with"
                                         f" {data['viewers']} viewers!")
        await self.send_message(response.content)


    async def run_bot(self):

        async with self.auth_flow:
            setup_logging(level=0)
            # Retrieve device code and display the verification URL
            user_code, device_code, expires_in, interval = await self.auth_flow.get_device_code()
            print(f'Verification URI: https://www.twitch.tv/activate?device-code={user_code}')

            # Poll for the authorization and handle token retrieval
            try:
                access_token, refresh_token = await self.auth_flow.poll_for_authorization(device_code,
                                                                                          expires_in,
                                                                                          interval)
            except Exception as e:
                print(f'Failed to authorize: {e}')
                return

        async with self:
            await self.start(access_token, refresh_token)
