from aiogram.types import Message
from openai import OpenAI

from src.config import settings, sys_prompt


# prompt = """Ты - бот в комментариях в канале с артами.
# Твоя задача отвечать пользователям.
# Ты играешь роль и не должен из неё выходить.
#
# Твоя роль: Ты антропоморфный лис по имени Арбузик.
#
# Следующим сообщением будет пост в канале, а далее ваша переписка с пользователями.
# Пользователей несколько. Учитывай это в своих ответах, понимая, кому именно ты отвечаешь.
# """

def prepare_message(
    msg: Message,
) -> str:
    if msg.from_user.id == settings.tg_owner_id:
        result = f"[Тоша"
    else:
        result = f"[{msg.from_user.full_name}"
    if msg.reply_to_message:
        if msg.reply_to_message.from_user.id == settings.tg_owner_id:
            result += f" (отвечает Тоше)"
        else:
            result += f" (отвечает {msg.reply_to_message.from_user.full_name})"
    result += "]:\n"
    if msg.photo:
        result += "<Изображение>\n"
    if msg.text:
        result += msg.text
    return result


def remove_duplicates(msgs: list[Message]) -> list[Message]:
    seen_ids = set()
    unique_data = []

    for item in msgs:
        if item.message_id not in seen_ids:
            unique_data.append(item)
            seen_ids.add(item.message_id)
    return unique_data


async def generate_prompt(
    user_message: Message,
    post: Message | None,
    thread: list[Message],
    neighbours: list[Message],
    bot_id: int
) -> list[tuple[str, str]]:  # role | msg
    result: list[tuple[str, str]] = [("SYSTEM", sys_prompt)]
    if post:
        result.append(("USER", prepare_message(post)))
    all_msgs = thread + neighbours + [user_message]
    all_msgs = [msg for msg in all_msgs if msg is not None]
    all_msgs = sorted(all_msgs, key=lambda item: item.date)
    all_msgs = remove_duplicates(all_msgs)
    all_msgs = all_msgs[-settings.max_input_msgs:]
    for msg in all_msgs:
        result.append(("USER" if msg.from_user.id != bot_id else "ASSISTANT", prepare_message(msg)))
    return result


aicli = OpenAI(
    api_key= settings.openai_api_key.get_secret_value(),
    base_url=settings.openai_base_url,
)

async def get_response(data: list[tuple[str, str]]) -> str:
    msgs = [
        {"role": role, "content": text}
        for role, text in data
    ]
    result = aicli.chat.completions.create(
        messages=msgs,  # type: ignore
        model="llama-3.3-70b-instruct", # "grok-3-mini-beta",
        max_tokens=1000,
    )
    result = result.choices[0].message.content
    if "[Arbuzik-AI" in result or "[Арбу" in result:
        result = "\n".join(result.split("\n")[1:])
    return result
