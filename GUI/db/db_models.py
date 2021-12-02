from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, create_engine, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    messages = relationship("Message", backref=backref("user"))

    def __str__(self):
        return f'User({self.user_id}, {self.username})'

    def __repr__(self):
        return str(self)

    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }


class Chat(Base):
    __tablename__ = "chat"
    chat_id = Column(Integer, primary_key=True)
    name = Column(String)
    messages = relationship("Message", backref=backref("chat"), order_by="Message.time")

    def __str__(self):
        return f'Chat({self.chat_id}, {self.name})'

    def __repr__(self):
        return str(self)


class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chat.chat_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    body = Column(String)
    time = Column(DateTime)
    is_sent = Column(Boolean, default=False)

    def __str__(self):
        return f'Message({self.message_id}, {self.user_id} -> {self.chat_id}) = {self.body}'

    def __repr__(self):
        return str(self)


def get_session():
    engine = create_engine('sqlite:////Users/path_to_this_file/chat.db') #TODO Путь до БД
    Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
    Session = sessionmaker(bind=engine)
    return Session()


session = get_session()
