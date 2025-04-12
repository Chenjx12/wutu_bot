import asyncio
import aiomysql
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg, ArgPlainText
from nonebot.typing import T_State
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "x121281",
    "db": "lianshi",
    "charset": "utf8mb4",
    "autocommit": True
}

# 创建数据库连接池
async def create_pool():
    return await aiomysql.create_pool(**DB_CONFIG)

# 从数据库中获取问题
async def get_question(pool):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT id, questions, optionA, optionB, optionC, optionD, answer, mohun FROM xuanze ORDER BY RAND() LIMIT 1")
            return await cursor.fetchone()

# 检查答案是否正确
async def check_answer(pool, question_id, user_answer):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT answer FROM xuanze WHERE id = %s", (question_id,))
            result = await cursor.fetchone()
            return result["answer"].strip().lower() == user_answer.strip().lower()

# 问答命令
qa_matcher = on_command("ls", aliases={"联诗", "开始联诗"}, priority=5, block=True)

@qa_matcher.handle()
async def handle_qa(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    user_id = event.get_user_id()
    if "qa_sessions" not in state:
        state["qa_sessions"] = {}
    qa_sessions = state["qa_sessions"]

    if user_id in qa_sessions:
        await bot.send(event, MessageSegment.at(user_id) + " 你已经在进行问答了，请先完成当前的问答。")
        return

    # 创建数据库连接池
    pool = await create_pool()
    qa_sessions[user_id] = {"pool": pool}

    # 获取用户指定的问答次数，默认为5次（测试使用3次）
    args_text = args.extract_plain_text().strip()
    try:
        max_rounds = int(args_text) if args_text.isdigit() else 3
        max_rounds = max(3, min(max_rounds, 20))  # 限制问答次数在3-20次之间
    except ValueError:
        max_rounds = 3

    qa_sessions[user_id]["rounds"] = 0
    qa_sessions[user_id]["max_rounds"] = max_rounds
    qa_sessions[user_id]["start_time"] = datetime.now()  # 记录开始时间

    # 获取第一个问题
    one_question = await get_question(pool)
    if not one_question:
        await bot.send(event, MessageSegment.at(user_id) + " 问题库为空，请联系管理员添加问题")
        return

    qa_sessions[user_id]["question_id"] = one_question["id"]
    qa_sessions[user_id]["rounds"] += 1
    current_round = qa_sessions[user_id]["rounds"]
    max_rounds = qa_sessions[user_id]["max_rounds"]

    question_text = (
        MessageSegment.at(user_id) + f" 当前轮次：{current_round}/{max_rounds}\n" +
        f"id:{one_question['id']}\n 所属墨魂:{one_question['mohun']}" +
        f"{one_question['questions']}\n" +
        f"A:{one_question['optionA']} B:{one_question['optionB']}\n" +
        f"C:{one_question['optionC']} D:{one_question['optionD']}"
    )
    await bot.send(event, question_text)

@qa_matcher.got("answer")
async def handle_answer(bot: Bot, event: Event, state: T_State, answer: str = ArgPlainText("answer")):
    user_id = event.get_user_id()
    if "qa_sessions" not in state or user_id not in state["qa_sessions"]:
        await bot.send(event, MessageSegment.at(user_id) + " 你没有正在进行的问答。")
        return

    qa_sessions = state["qa_sessions"]
    session = qa_sessions[user_id]
    user_answer = str(answer).strip()
    pool = session["pool"]
    rounds = session["rounds"]
    max_rounds = session["max_rounds"]

    # 检查是否是退出指令
    if user_answer in ["/退出", "/结束", "退出", "结束"]:
        await bot.send(event, MessageSegment.at(user_id) + " 问答已结束！")
        del qa_sessions[user_id]
        return

    if await check_answer(pool, session["question_id"], user_answer):
        await bot.send(event, MessageSegment.at(user_id) + " 回答正确！")
        rounds += 1
        session["rounds"] = rounds

        if rounds <= max_rounds:
            next_question = await get_question(pool)
            session["question_id"] = next_question["id"]
            session["rounds"] = rounds
            current_round = rounds
            question_text = (
                MessageSegment.at(user_id) + f" 当前轮次：{current_round}/{max_rounds}\n" +
                f"id:{next_question['id']} 所属墨魂:{next_question['mohun']}\n" +
                f"{next_question['questions']}\n" +
                f"A:{next_question['optionA']} B:{next_question['optionB']}\n" +
                f"C:{next_question['optionC']} D:{next_question['optionD']}"
            )
            await bot.send(event, question_text)
            await qa_matcher.reject()  # 重新进入等待状态
        else:
            # 用户完成所有问答，计算总时间
            end_time = datetime.now()
            start_time = session["start_time"]
            total_time = (end_time - start_time).total_seconds()

            if total_time <= 10:
                evaluation = "优"
            elif 10 < total_time <= 15:
                evaluation = "良"
            else:
                evaluation = "一般"

            await bot.send(event, MessageSegment.at(user_id) + f" 恭喜你，完成了{max_rounds}次，联诗结束！\n"
                                                              f"总用时：{total_time:.2f}秒，评价：{evaluation}")
            del qa_sessions[user_id]
    else:
        await bot.send(event, MessageSegment.at(user_id) + " 回答错误，请再试一次！")
        await qa_matcher.reject()  # 重新进入等待状态，让用户重新回答当前问题