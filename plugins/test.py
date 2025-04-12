from nonebot import on_regex
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot, Message, MessageEvent

import pymysql

Test = on_regex(pattern=r'^测试$',rule=to_me(),priority=1)
# Test = on_command("测试", rule=to_me(), priority=1, block=True)

@Test.handle()
async def Test_send(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.user_id
    nickname = event.sender.card or event.sender.nickname
    reply_msg = f""
 #   await Test.send(Message.reply(event.message_id) + MessageSegment.text(reply_msg))
#    await Test.finish(MessageSegment.at(user_id))
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='x121281',
                     database='qqbot')
    
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    # print("Database version : %s " % data)
    # 关闭数据库连接
    db.close()

    await Test.finish(Message(f"[CQ:reply,id={event.message_id}] [CQ:at,qq={user_id}] Bot启动正常，数据库版本：{data} 数据库连接正常\n 爱莉爱莉爱~"))


User_Help = on_regex(pattern=r'^help$', rule=to_me(), priority=1, block=True)
@User_Help.handle()
async def uh_send(bot: Bot, event: GroupMessageEvent, state: T_State):
    await User_Help.finish(MessageSegment.reply(event.message_id) +
                         "\n@菟菟 测试：测试bot是否正常运行\n"
                         "@菟菟 点卯：进行每日点卯\n"
                         "@菟菟 /ls, /联诗 /开始联诗 num xx：可以和菟菟开始联诗，num为题量，默认3道题，最多20，群聊@，私聊则无需@（题库完善中\n"
                         "大饼：指定墨魂联诗、使用\"*\"则大杂烩\n"
                         "@菟菟 兰台小筑：可以查看兰台小筑照片\n"
                         "@菟菟 飞花令：可以开始飞花令，群聊菟菟当裁判，私聊则和菟菟pk（这是大饼\n"
                         "@菟菟 xx魂设：自行替换xx为魂名，菟菟回应官方一图流魂设（还没写但是很快\n"
                         "注：未写明可以私聊的统统只能在群内@响应")
