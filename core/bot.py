from twitch.ext.oauth import DeviceAuthFlow, Scopes
from twitch.errors import Forbidden
from twitch.user import Broadcaster
from twitch.types import eventsub
from twitch.ext.bot import Bot

class Twitch(Bot):
    def __init__(self, client_id: str):
        super().__init__(client_id)

    async def setup_hook(self) -> None:
        pass

    async def on_chat_message(self, data: eventsub.chat.MessageEvent):
        ...

    async def on_chat_clear(self, data: eventsub.chat.ChatClearEvent):
        ...

    async def on_shared_chat_begin(self, data: eventsub.chat.SharedChatBeginEvent):
        ...

    async def on_shared_chat_end(self, data: eventsub.chat.SharedChatEndEvent):
        ...

    async def on_cheer(self, data: eventsub.bits.CheerEvent):
     ...

    async def on_channel_update(self, data: eventsub.channels.ChannelUpdateEvent):
        ...

    async def on_follow(self, data: eventsub.channels.FollowEvent):
        ...

    async def on_subscribe(self, data: eventsub.channels.SubscribeEvent):
        ...

    async def on_subscription_end(self, data: eventsub.channels.SubscriptionEndEvent):
        ...

    async def on_subscription_gift(self, data: eventsub.channels.SubscriptionGiftEvent):
        ...

    async def on_subscription_message(self, data: eventsub.channels.SubscriptionMessageEvent):
        ...

    async def on_poll_begin(self, data: eventsub.interaction.PollBeginEvent):
        ...

    async def on_poll_end(self, data: eventsub.interaction.PollEndEvent):
        ...

    async def on_prediction_begin(self, data: eventsub.interaction.PredictionBeginEvent):
        ...

    async def on_prediction_lock(self, data: eventsub.interaction.PredictionLockEvent):
        ...

    async def on_prediction_end(self, data: eventsub.interaction.PredictionEndEvent):
        ...

    async def on_hype_train_begin(self, data: eventsub.interaction.HypeTrainEvent):
        ...

    async def on_hype_train_end(self, data: eventsub.interaction.HypeTrainEndEvent):
        ...

    async def on_raid(self, data: eventsub.streams.RaidEvent):
        ...

    async def on_shoutout_create(self, data: eventsub.streams.ShoutoutCreateEvent):
        ...

    async def on_stream_online(self, data: eventsub.streams.StreamOnlineEvent):
        ...

    async def on_stream_offline(self, data: eventsub.streams.StreamOfflineEvent):
        ...