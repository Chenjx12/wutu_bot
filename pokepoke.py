from nonebot import on_notice
import json
from nonebot.adapters.onebot.v11 import Bot, PokeNotifyEvent

# 注册一个通知事件响应器
poke = on_notice()

@poke.handle()
async def handle_poke(bot: Bot, event: PokeNotifyEvent):
    # 判断是否是戳一戳事件
    if event.notice_type == "notify" and event.sub_type == "poke":
        # 判断是否是戳机器人
        if event.target_id == event.self_id:
            # 获取戳机器人的人的信息
            user_id = event.user_id
            group_id = event.group_id
            # 发送戳一戳响应
            if group_id:  # 如果是群聊
                await bot.send(event,"喵~")
                await bot.call_api(api="send_poke",
                    user_id=user_id,
                    group_id=group_id)
            else:  # 如果是私聊
                await bot.send(event,"喵~")