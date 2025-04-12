from nonebot import on_message
from nonebot.adapters import Message
from nonebot.rule import to_me, Rule
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import PrivateMessageEvent,GroupMessageEvent,Event

def is_group_message(event: Event) -> bool:
    return isinstance(event, PrivateMessageEvent)

private_message_rule = Rule(is_group_message)

private_chat = on_message(rule=private_message_rule, priority=5, block=False)

@private_chat.handle()
async def handle_private_chat(event: PrivateMessageEvent, state: T_State):
    # 获取消息内容
    message = event.get_message()
    # 可以在这里处理消息，例如回复用户
    await private_chat.send("(测试）你好，这是私聊回复！")
