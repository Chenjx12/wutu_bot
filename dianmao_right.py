
from nonebot import on_regex
from nonebot.rule import to_me, Rule
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment, Bot, Message, Event

import pymysql
from datetime import datetime, timedelta

# 定义一个检查消息是否来自群聊的规则
def is_group_message(event: Event) -> bool:
    return isinstance(event, GroupMessageEvent)

# 创建一个Rule实例，用于组合多个规则
group_message_rule = Rule(is_group_message)

# 仅响应群聊中的@
Test1 = on_regex(pattern=r'^点卯$',rule=to_me() & group_message_rule,priority=5)
# Test = on_command("测试", rule=to_me(), priority=1, block=True)

@Test1.handle()
async def Test1_send(bot: Bot, event: GroupMessageEvent, state: T_State):
    user_id = event.user_id
    nickname = event.sender.card or event.sender.nickname
    reply_msg = f""
 #   await Test.send(Message.reply(event.message_id) + MessageSegment.text(reply_msg))
#    await Test.finish(MessageSegment.at(user_id))
    db = pymysql.connect(host='localhost',
                     user='myadmin',
                     password='password',
                     database='qqbot')
    
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS dianmao (
            兰台昵称 VARCHAR(255) NOT NULL,
            qq_id BIGINT NOT NULL,
            连续点卯天数 INT NOT NULL DEFAULT 0,
            总点卯天数 BIGINT NOT NULL DEFAULT 0,
            上一次点卯时间 TIMESTAMP NOT NULL,
            归斋时间 DATE NOT NULL,
            PRIMARY KEY (qq_id)
        )
        """

    cursor.execute(create_table_sql)
    
    alter_table_query = """
    ALTER TABLE dianmao MODIFY 上一次点卯时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
    """
    cursor.execute(alter_table_query)

    cursor.execute("SELECT 上一次点卯时间 FROM dianmao WHERE qq_id = %s", (user_id,))
    result = cursor.fetchone()

    now = datetime.now()
    start_of_last_day = now.replace(hour=4, minute=0, second=0, microsecond=0)

    if now < start_of_last_day:
        # 说明现在是0-4点
        start_of_last_day = start_of_last_day - timedelta(days=1)
    
    end_of_last_day = start_of_last_day + timedelta(days=1)

    # 如果存在上一次点卯，说明数据库中存在该信息，result不可能为none，如果为none，就跳过点卯验证环节，直接去下面insert新的用户数据
    if result:
        # last_dianmao_time = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        # 如果上一次点卯时间在今天凌晨四点之后，则不允许再次点卯
        if start_of_last_day <= result[0] < end_of_last_day:
            db.close()
            await Test1.finish(Message(f"[CQ:reply,id={event.message_id}] [CQ:at,qq={user_id}] 兰台今天已经点卯过了喵，请明天再来"))
            return
        if result[0] - end_of_last_day < timedelta(days=1):
            # 用户在相邻的两天内点卯，连续点卯天数增加
            continuous_days = "连续点卯天数 + 1"
        else:
            # 用户没有在相邻的两天内点卯，连续点卯天数重置为1
            continuous_days = 1
    else:
        continuous_days = 1
    

    # 点卯成功
    insert_update_sql = f"""
        INSERT INTO qqbot.dianmao (兰台昵称, qq_id, 连续点卯天数, 总点卯天数, 上一次点卯时间, 归斋时间)
        VALUES (%s, %s, 1, 1, CURRENT_TIMESTAMP, CURRENT_DATE)
        ON DUPLICATE KEY UPDATE
          连续点卯天数 = {continuous_days},
          总点卯天数 = 总点卯天数 + 1,
          上一次点卯时间 = CURRENT_TIMESTAMP,
          归斋时间 = IF(总点卯天数 = 0, CURRENT_DATE, 归斋时间);
        """

    cursor.execute(insert_update_sql, (nickname, user_id))

    cursor.execute("SELECT 连续点卯天数 FROM dianmao WHERE qq_id = %s", (user_id,))
    days = cursor.fetchone()

    cursor.execute("SELECT 总点卯天数 FROM dianmao WHERE qq_id = %s", (user_id,))
    all_days = cursor.fetchone()

    db.commit()
    # 关闭数据库连接
    db.close()

    await Test1.finish(Message(f"[CQ:reply,id={event.message_id}] [CQ:at,qq={user_id}] 喵~ 兰台点卯成功~\n已连续点卯{days}天\n共点卯{all_days}天"))
