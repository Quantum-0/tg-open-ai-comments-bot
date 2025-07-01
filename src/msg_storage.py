from aiogram.types import Message

all_messages: dict[int, Message] = {}

def save_message(msg: Message):
    all_messages[msg.message_id] = msg

def get_message(message_id: int) -> Message | None:
    return all_messages.get(message_id)

def get_thread(msg: Message) -> list[Message]:
    queue: list[int] = [msg.message_id]
    while True:
        if msg.reply_to_message:
            queue.append(msg.reply_to_message.message_id)
            msg = get_message(msg.reply_to_message.message_id)
            if msg is None:
                break
        else:
            break
    return [get_message(msg_id) for msg_id in queue[::-1]]

def get_neighbours(msg: Message) -> list[Message]:
    neighbours = []
    for other_msg in all_messages.values():
        if msg.reply_to_message:
            if other_msg.reply_to_message:
                if other_msg.reply_to_message.message_id == msg.reply_to_message.message_id:
                    if msg.message_id != other_msg.message_id:
                        neighbours.append(other_msg)
        elif msg.message_thread_id == other_msg.message_thread_id:
            if not other_msg.reply_to_message and msg.message_id != other_msg.message_id:
                neighbours.append(other_msg)
    return neighbours