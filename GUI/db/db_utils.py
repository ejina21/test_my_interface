import datetime

from test_my_interface.GUI.db.db_models import session, User, Chat, Message


def get(model, **kwargs):
    return session.query(model).filter_by(**kwargs).first()


def create(model, **kwargs):
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


def get_or_create(model, **kwargs):
    return get(model, **kwargs) or create(model, **kwargs)


def create_myself(**kwargs):
    return create(User, user_id=1, **kwargs)


def get_myself():
    return get(User, user_id=1)


def get_or_create_user(**kwargs):
    return get_or_create(User, **kwargs)


def get_users():
    return session.query(User).order_by(User.username).all()


def get_or_create_chat(user):
    return get_or_create(Chat, chat_id=user.user_id, name=user.username)


def get_chats():
    return session.query(Chat).order_by(Chat.chat_id).all()


def create_message(chat, user, **kwargs):
    now = datetime.datetime.now()
    message = Message(chat_id=chat.chat_id, user_id=user.user_id, time=now, **kwargs)
    session.add(message)
    session.commit()
    return message


def send_message(chat, body=''):
    my_user = get_myself()
    send_to = get(User, user_id=chat.chat_id)
    # is_sent = send_message_to_user()  # TODO: create
    is_sent = False
    return create_message(chat, user=my_user, body=body, is_sent=is_sent)


def main():
    user1 = get_or_create_user(username='user_1', first_name=f'first_name_1', last_name=f'last_name_1')
    for i in range(2, 30):
        user = get_or_create_user(username=f'user_{i}', first_name=f'first_name_{i}', last_name=f'last_name_{i}')
        chat = get_or_create_chat(user)
        for k in range(50):
            create_message(chat, user1, body=f'{k} message from {user1.user_id}')
            # print(chat1.messages)
            create_message(chat, user, body=f'{k} message from {user.user_id}')
            # print(chat1.messages)


if __name__ == '__main__':
    main()
