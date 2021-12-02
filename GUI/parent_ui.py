import asyncio
import json
from multiprocessing import Queue
from asyncio import Queue as aQueue

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath

from child_ui import newWindow
from test_my_interface.GUI.db.db_models import User, Chat as myChat
from test_my_interface.GUI.db.db_utils import get_chats, get, get_myself, send_message as sm

d_list = ["Привет, добрый день, здравтсуйте, кто сегодян победит? Тот, кто не уснет? Наверное, да!",
        "Как дела?",
        "Привет, добрый день, здравтсуйте, кто сегодян победит? Тот, кто не уснет? Наверное, да! тцаилрт удцлоатдтц цуоатдтй уацй уатжт жлцуьтл йтуатйу ",
        "Как дела?",
        ]
list = []
for i in range(20):
    for d in d_list:
        list.append(str(i) + " " + d)


class Ui_chat(object):

    def __init__(self, chat, queue_from_ui: aQueue=None, queue_from_core: Queue=None):
        self.chat_id = None
        self.chat_i = None
        self.queue_from_ui = queue_from_ui
        self.queue_from_core = queue_from_core
        chat.setObjectName("chat")
        chat.resize(901, 600)
        chat.setMinimumSize(QtCore.QSize(901, 600))
        chat.setMaximumSize(QtCore.QSize(901, 600))
        chat.setStyleSheet("background-color: #fff")
        self.centralwidget = QtWidgets.QWidget(chat)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_right = QtWidgets.QWidget(self.centralwidget)
        self.widget_right.setGeometry(QtCore.QRect(271, 0, 630, 600))
        self.widget_right.setObjectName("widget_right")
        self.widget_draw_line = QtWidgets.QWidget(self.centralwidget)
        self.widget_draw_line.setGeometry(QtCore.QRect(270, 0, 1, 600))
        self.widget_draw_line.setStyleSheet("background-color: #C2C2C2;")
        self.widget_right.setStyleSheet("border-left: 2px solid #C2C2C2;")
        self.widget_button_bot = QtWidgets.QWidget(self.widget_right)
        self.widget_button_bot.setGeometry(QtCore.QRect(-1, 550, 630, 50))
        self.widget_button_bot.setStyleSheet("background-color: #EFFFEF; border-top: 1px solid #C2C2C2;")
        self.widget_button_bot.setObjectName("widget_button_bot")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.widget_left = QtWidgets.QWidget(self.centralwidget)
        self.widget_left.setGeometry(QtCore.QRect(0, 0, 270, 600))
        self.widget_left.setObjectName("widget_left")
        self.widget_self_info = QtWidgets.QWidget(self.widget_left)
        self.widget_self_info.setGeometry(QtCore.QRect(0, 0, 270, 80))
        self.widget_self_info.setStyleSheet("background-color: #EFFFEF;")
        self.widget_self_info.setObjectName("widget_self_info")

        self.line_search = QtWidgets.QLineEdit(self.widget_left)
        self.line_search.setGeometry(QtCore.QRect(0, 80, 270, 30))
        self.line_search.setStyleSheet("background-color: #D4F8D4; color: #9BB49B; border: none;")
        self.line_search.setMaxLength(150)
        self.line_search.setCursorPosition(0)
        self.line_search.setObjectName("line_search")
        self.line_search.setPlaceholderText("  Поиск")
        self.line_search.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.users_chat_list()
        self.auto_size_message()
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        chat.setCentralWidget(self.centralwidget)

        self.retranslateUi(chat)
        QtCore.QMetaObject.connectSlotsByName(chat)

        self.add_users_chat_list_action()
        self.init_header_chat()
        self.create_button_add_people()
        self.init_my_info()
        self.create_textbox_and_button()

        # self.timer_status = QtCore.QTimer()
        # self.timer_status.timeout.connect(self.update_all_views)
        # self.timer_status.start(1000)

    def update_all_views(self):
        print('update all views')
        lst_data = []
        try:
            while data := self.queue_from_core.get_nowait():
                lst_data.append(data)
        except Exception as e:
            print('Error update_all_views')
            print(e)

    async def a_send_core_message(self, message):
        await self.queue_from_ui.put(message)

    def send_core_message(self, message):
        asyncio.get_event_loop().run_until_complete(self.a_send_core_message(message))

    def draw_message(self, chat_id=2, text=''):
        pass
        # if len(text) == 0:
        #     return
        # chat = get(myChat, chat_id=chat_id)
        # sm(chat, text)
        # self.ui.scroll_for_message.deleteLater()
        # self.ui.auto_size_message(chat_id=chat_id, create=True)

    my_dict = {'url': 'src/self2.jpg', 'my_name': 'Никита Ежин', 'my_status': 'В сети'}
    peer_dict = {'url': 'src/self.jpg', 'peer_name': 'Стас Мощь', 'peer_status': 'был(a) в сети недавно'}

    def init_my_info(self):
        user = get_myself().get_dict()
        self.my_photo = QtWidgets.QLabel(self.widget_self_info)
        self.my_photo.setMaximumSize(40, 40)
        self.my_photo.setMinimumSize(40, 40)
        self.my_photo.move(40, 20)

        self.my_target = QPixmap(self.my_photo.size())
        self.my_target.fill(Qt.transparent)

        p = QtGui.QPixmap(self.my_dict['url']).scaled(
            40, 40, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter = QPainter(self.my_target)
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, 40, 40, 20, 20)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.my_photo.setPixmap(self.my_target)
        self.my_photo.setStyleSheet("border: none;")

        self.my_name = QtWidgets.QLabel(self.widget_self_info)
        self.my_name.setGeometry(QtCore.QRect(95, 25, 150, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setBold(True)
        self.my_name.setFont(font)
        self.my_name.setStyleSheet("color: rgb(115, 154, 111); border: none;")
        self.my_name.setObjectName("my_name")
        self.my_status = QtWidgets.QLabel(self.widget_self_info)
        self.my_status.setGeometry(QtCore.QRect(95, 40, 150, 16))
        font.setPointSize(11)
        font.setBold(False)
        self.my_status.setFont(font)
        self.my_status.setStyleSheet("color: rgb(115, 154, 111); border: none;")
        self.my_status.setObjectName("my_status")
        self.my_name.setText(str(user['first_name']) + ' ' + str(user['last_name']))
        self.my_status.setText(self.my_dict['my_status'])

    def create_button_add_people(self):
        self.button_add = QtWidgets.QPushButton(self.widget_self_info)
        self.button_add.setGeometry(QtCore.QRect(5, 5, 20, 20))
        self.button_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_add.setStyleSheet("border: none;")
        self.button_add.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src/add_people.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add.setIcon(icon1)
        self.button_add.setIconSize(QtCore.QSize(40, 40))
        self.button_add.setObjectName("button_add")

    def create_textbox_and_button(self):
        self.line_write_text = QtWidgets.QLineEdit(self.widget_button_bot)
        self.line_write_text.setGeometry(QtCore.QRect(60, 5, 450, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.line_write_text.setFont(font)
        self.line_write_text.setStyleSheet("""color: #9BB49B; border: none;""")
        self.line_write_text.setCursorPosition(0)
        self.line_write_text.setObjectName("line_write_text")
        self.line_write_text.setPlaceholderText("   Введите текст...")
        self.line_write_text.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.send_button = QtWidgets.QPushButton(self.widget_button_bot)
        self.send_button.setGeometry(QtCore.QRect(580, 5, 40, 40))
        self.send_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.send_button.setStyleSheet("border: none;")
        self.send_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('src/send_icon.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.send_button.setIcon(icon)
        self.send_button.setIconSize(QtCore.QSize(25, 25))
        self.send_button.setObjectName("send_button")
        self.emoji_button = QtWidgets.QPushButton(self.widget_button_bot)
        self.emoji_button.setGeometry(QtCore.QRect(530, 5, 40, 40))
        self.emoji_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.emoji_button.setStyleSheet("border: none;")
        self.emoji_button.setText("")
        icon.addPixmap(QtGui.QPixmap('src/emoji.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.emoji_button.setIcon(icon)
        self.emoji_button.setIconSize(QtCore.QSize(30, 30))
        self.emoji_button.setObjectName("emoji_button")
        self.file_button = QtWidgets.QPushButton(self.widget_button_bot)
        self.file_button.setGeometry(QtCore.QRect(10, 5, 40, 40))
        self.file_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.file_button.setStyleSheet("border: none;")
        self.file_button.setText("")
        icon.addPixmap(QtGui.QPixmap('src/file.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.file_button.setIcon(icon)
        self.file_button.setIconSize(QtCore.QSize(25, 25))
        self.file_button.setObjectName("file_button")

    def clear_messages(self):
        self.scroll_for_message.deleteLater()
        self.widget_info_peer.deleteLater()

    def auto_size_message(self, create=False):
        my_chat = get(myChat, chat_id=self.chat_id)
        max_symbols = 41
        message_high = 40
        message_wight = 300
        message_delta = 10
        scroll_for_message_message_wight = 630
        scroll_for_message_message_high = 490
        list_dict = []
        self.scroll_for_message = QtWidgets.QScrollArea(self.widget_right)
        self.scroll_for_message.setGeometry(
            QtCore.QRect(
                0, 60, scroll_for_message_message_wight, scroll_for_message_message_high
            )
        )
        self.scroll_for_message.setStyleSheet("border: none; background-color: rgb(111, 178, 101);")
        self.scroll_for_message.setObjectName("scroll_for_message")
        self.scroll_for_message.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        if my_chat is None:
            return
        full_hight = 0
        messages = my_chat.messages

        print(f'{messages=}')
        for el in messages:
            dict_message = {}
            dict_message['count_line'] = len(el.body) // max_symbols + 1
            full_hight += dict_message['count_line'] * (message_high - 20) + message_delta + 20
            dict_message['message'] = el.body
            dict_message['whome'] = 'self' if el.user_id == 1 else None
            dict_message['time'] = el.time.strftime('%H:%M')
            list_dict.append(dict_message)
        self.scroll_for_message_contents = QtWidgets.QWidget()
        self.scroll_for_message_contents.setGeometry(
            QtCore.QRect(0, 0, scroll_for_message_message_wight, full_hight + 10))
        self.scroll_for_message_contents.setObjectName("scroll_for_message_contents")
        i = 0
        lenght = 0
        for el in list_dict:
            i += 1
            message_high_el = el['count_line'] * (message_high - 20) + 20

            setattr(
                self,
                f'message_widget_contents_{i}',
                QtWidgets.QWidget(self.scroll_for_message_contents)
            )  # Создали новый виджет под каждое сообщение
            if el['whome'] == 'self':  # TODO:
                getattr(
                    self,
                    f'message_widget_contents_{i}'
                ).setGeometry(
                    QtCore.QRect(
                        scroll_for_message_message_wight - 10 - message_wight,
                        message_delta + lenght, message_wight, message_high_el
                    )
                )
                getattr(
                    self,
                    f'message_widget_contents_{i}'
                ).setStyleSheet("""background-color: rgb(255, 255, 255); 
                            border: none; border-top-left-radius: 20px;
                            border-top-right-radius: 20px;
                            border-bottom-left-radius: 20px;
                            border-bottom-right-radius: 0""")
            else:
                getattr(
                    self,
                    f'message_widget_contents_{i}'
                ).setGeometry(
                    QtCore.QRect(
                        10, message_delta + lenght, message_wight, message_high_el
                    )
                )
                getattr(
                    self,
                    f'message_widget_contents_{i}'
                ).setStyleSheet("""background-color: rgb(227, 249, 223); 
                            border: none; border-top-left-radius: 20px;
                            border-top-right-radius: 20px;
                            border-bottom-right-radius: 20px;
                            border-bottom-left-radius: 0;
                            """)
            getattr(
                self,
                f'message_widget_contents_{i}'
            ).setObjectName(f'message_widget_contents_{i}')

            """ Время сообщения """
            setattr(
                self,
                f'm_time_{i}',
                QtWidgets.QTextBrowser(getattr(self, f'message_widget_contents_{i}'))
            )
            getattr(
                self,
                f'm_time_{i}',
            ).setGeometry(QtCore.QRect(233, message_high_el - 15, 40, 20))
            getattr(
                self,
                f'm_time_{i}',
            ).setStyleSheet("color: rgb(115, 154, 111); border: none;")
            getattr(
                self,
                f'm_time_{i}',
            ).setObjectName(f'm_time_{i}')
            getattr(
                self,
                f'm_time_{i}',
            ).setHtml(
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                f"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">{el['time']}</span></p></body></html>")
            """ Текс сообщения"""
            setattr(
                self,
                f'm_text_{i}',
                QtWidgets.QTextBrowser(getattr(self, f'message_widget_contents_{i}'))
            )
            getattr(
                self,
                f'm_text_{i}',
            ).setGeometry(QtCore.QRect(7, 5, 286, 20 * el['count_line'] + 6))
            getattr(
                self,
                f'm_text_{i}',
            ).setStyleSheet("color: rgb(0, 0, 0); border: none;")
            getattr(
                self,
                f'm_text_{i}',
            ).setObjectName(f'm_text_{i}')
            getattr(
                self,
                f'm_text_{i}',
            ).setText(el['message'])  # TODO:
            lenght += message_high_el + message_delta

        self.scroll_for_message.setWidget(self.scroll_for_message_contents)
        x = self.scroll_for_message.verticalScrollBar().maximum()
        self.scroll_for_message.verticalScrollBar().setValue(x)
        if create:
            self.scroll_for_message.show()

    def init_header_chat(self, create=False):
        my_chat = get(myChat, chat_id=self.chat_id)
        self.widget_info_peer = QtWidgets.QWidget(self.widget_right)
        self.widget_info_peer.setGeometry(QtCore.QRect(-1, 0, 630, 60))
        self.widget_info_peer.setObjectName("widget_info_peer")
        self.widget_info_peer.setStyleSheet("background-color: #EFFFEF; border-bottom: 1px solid #C2C2C2;")
        self.peer_photo = QtWidgets.QLabel(self.widget_info_peer)
        self.peer_photo.setMaximumSize(40, 40)
        self.peer_photo.setMinimumSize(40, 40)
        self.peer_photo.move(30, 10)
        self.peer_target = QPixmap(self.peer_photo.size())
        self.peer_target.fill(Qt.transparent)

        p = QtGui.QPixmap(self.peer_dict['url']).scaled(
            40, 40, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter = QPainter(self.peer_target)
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, 40, 40, 20, 20)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.peer_photo.setStyleSheet("border: none;")
        self.peer_name = QtWidgets.QLabel(self.widget_info_peer)
        self.peer_name.setGeometry(QtCore.QRect(80, 15, 450, 16))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setBold(True)
        self.peer_name.setFont(font)
        self.peer_name.setStyleSheet("color: rgb(115, 154, 111); border: none;")
        self.peer_name.setObjectName("peer_name")
        self.peer_info = QtWidgets.QLabel(self.widget_info_peer)
        self.peer_info.setGeometry(QtCore.QRect(80, 30, 450, 16))
        font.setPointSize(11)
        font.setBold(False)
        self.peer_info.setFont(font)
        self.peer_info.setStyleSheet("color: rgb(115, 154, 111); border: none;")
        self.peer_info.setObjectName("peer_info")
        self.call_button = QtWidgets.QPushButton(self.widget_info_peer)
        self.call_button.setGeometry(QtCore.QRect(450, 10, 40, 40))
        self.call_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.call_button.setStyleSheet("border: none;")
        self.call_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('src/call.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.call_button.setIcon(icon)
        self.call_button.setIconSize(QtCore.QSize(25, 25))
        self.call_button.setObjectName("call_button")
        self.search_button = QtWidgets.QPushButton(self.widget_info_peer)
        self.search_button.setGeometry(QtCore.QRect(510, 10, 40, 40))
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.setStyleSheet("border: none;")
        self.search_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('src/search.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon)
        self.search_button.setIconSize(QtCore.QSize(25, 25))
        self.search_button.setObjectName("search_button")
        self.more_button = QtWidgets.QPushButton(self.widget_info_peer)
        self.more_button.setGeometry(QtCore.QRect(570, 0, 40, 50))
        self.more_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.more_button.setStyleSheet("border: none; color: #868686; font-size: 35px; text-align: top;")
        self.more_button.setText("...")
        self.more_button.setObjectName("search_button")
        if my_chat is None:
            return
        user = get(User, user_id=my_chat.chat_id).get_dict()
        self.peer_name.setText(str(user['first_name']) + ' ' + str(user['last_name']))
        self.peer_info.setText(self.peer_dict['peer_status'])
        self.peer_photo.setPixmap(self.peer_target)
        if create:
            self.widget_info_peer.show()

    def add_users_chat_list_action(self):
        i = 0
        while getattr(self, f'user_push_button_{i}', None):
            getattr(
                self,
                f'user_push_button_{i}'
            ).clicked.connect(self.users_chat_list_button_click)
            i += 1

    def users_chat_list_button_click(self):
        try:
            sender = self.centralwidget.sender()
            text = sender.text()
            print(text)
            json_acceptable_string = text.replace("\'", "\"")
            print(json_acceptable_string)
            d = json.loads(json_acceptable_string)
            print(f'{d=}')
            if self.chat_i is not None:
                getattr(
                    self,
                    f'user_widget_contents_{self.chat_i}'
                ).setStyleSheet("background-color: rgb(255, 255, 255);")
                getattr(
                    self,
                    f'user_last_message_{self.chat_i}'
                ).setStyleSheet("color: rgb(153, 153, 153);")
                getattr(
                    self,
                    f'user_name_{self.chat_i}'
                ).setStyleSheet("color: rgb(0, 0, 0);")
                getattr(
                    self,
                    f'user_last_message_time_{self.chat_i}'
                ).setStyleSheet("color: rgb(153, 153, 153);")
            getattr(
                self,
                f'user_widget_contents_{d["i"]}'
            ).setStyleSheet("background-color: rgb(82, 173, 64);")
            getattr(
                self,
                f'user_last_message_{d["i"]}'
            ).setStyleSheet("color: rgb(255, 255, 255);")
            getattr(
                self,
                f'user_name_{d["i"]}'
            ).setStyleSheet("color: rgb(255, 255, 255);")
            getattr(
                self,
                f'user_last_message_time_{d["i"]}'
            ).setStyleSheet("color: rgb(255, 255, 255);")
            self.chat_i = d['i']
            self.clear_messages()
            self.chat_id = d['chat']
            self.auto_size_message(True)
            self.init_header_chat(True)

            print(text)
            print(dir(sender))
        except Exception as e:
            print('Error')
            print(e)

    def users_chat_list(self, create=False):
        """ Список чатов слева"""

        user_high = 70

        chats = get_chats()
        users_count = len(chats)  # TODO:
        # users_count = 1
        print(chats)
        list_wight = 270
        self.scroll_users_area = QtWidgets.QScrollArea(self.widget_left)
        self.scroll_users_area.setGeometry(QtCore.QRect(0, 110, list_wight, 490))
        self.scroll_users_area.setObjectName("scroll_users_area")
        self.scroll_users_area.setStyleSheet("border: none;")
        self.scroll_users_area.setStyleSheet("border: none;\n")
        self.scroll_users_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scroll_users_area_widget_contents = QtWidgets.QWidget()  # Виджет для всего списка пользователей
        self.scroll_users_area_widget_contents.setGeometry(QtCore.QRect(0, 0, list_wight, (user_high + 5) * users_count))  # TODO:
        self.scroll_users_area_widget_contents.setObjectName("scroll_users_area_widget_contents")

        for i in range(users_count):
            chat = chats[i]
            # i = chat.chat_id
            # print(i)
            # print(get(User, user_id=i).get_name())
            setattr(
                self,
                f'user_widget_contents_{i}',
                QtWidgets.QWidget(self.scroll_users_area_widget_contents)
            )  # Создали новый виджет под каждого пользователя
            getattr(
                self,
                f'user_widget_contents_{i}'
            ).setGeometry(QtCore.QRect(0, i * (user_high + 5), list_wight, user_high))
            # getattr(
            #     self,
            #     f'user_widget_contents_{i}'
            # ).setStyleSheet('background-color: rgb(167, 238, 255);')

            """ Имя юзера """
            setattr(
                self, f'user_name_{i}',
                QtWidgets.QTextBrowser(
                    getattr(self, f'user_widget_contents_{i}')
                )
            )  # Добавляем текст
            getattr(
                self,
                f'user_name_{i}'
            ).setGeometry(QtCore.QRect(50, 20, 259, int(user_high * 0.3)))
            getattr(
                self,
                f'user_name_{i}'
            ).setStyleSheet("color: rgb(0, 0, 0);")

            getattr(
                self,
                f'user_name_{i}'
            ).setObjectName(f"user_name_{i}")

            getattr(
                self,
                f'user_name_{i}'
            ).setHtml(
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">{get(User, user_id=chat.chat_id).get_name()}</span></p></body></html>")

            # getattr(
            #     self,
            #     f'user_name_{i}'
            # ).setText(f"user_last_message_{i}")  # TODO: тут заменить на имя из базы
            try:
                last_message = chat.messages[-1]
            except IndexError:
                last_message = None
            """ Последнее сообщение """
            setattr(
                self, f'user_last_message_{i}',
                QtWidgets.QTextBrowser(
                    getattr(self, f'user_widget_contents_{i}')
                )
            )  # Добавляем текст
            getattr(
                self,
                f'user_last_message_{i}'
            ).setGeometry(QtCore.QRect(50, 40, 259, int(user_high * 0.4)))
            getattr(
                self,
                f'user_last_message_{i}'
            ).setStyleSheet("color: rgb(153, 153, 153); background-color: rgba(255, 255, 255, 0);")

            getattr(
                self,
                f'user_last_message_{i}'
            ).setObjectName(f"user_last_message_{i}")

            getattr(
                self,
                f'user_last_message_{i}'
            ).setHtml(
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">{self.strim(last_message.body if last_message else '')}</span></p></body></html>")
            # getattr(
            #     self,
            #     f'user_last_message_{i}'
            # ).setText(f"user_last_message_{i}")  # TODO: тут заменить на имя из базы

            """ Время последнего сообщения сообщение """
            setattr(
                self, f'user_last_message_time_{i}',
                QtWidgets.QTextBrowser(
                    getattr(self, f'user_widget_contents_{i}')
                )
            )  # Добавляем текст
            getattr(
                self,
                f'user_last_message_time_{i}'
            ).setGeometry(QtCore.QRect(180, 43, 70, 30))
            getattr(
                self,
                f'user_last_message_time_{i}'
            ).setStyleSheet("color: rgb(153, 153, 153); border: none; background-color: rgba(255, 255, 255, 0);")

            getattr(
                self,
                f'user_last_message_time_{i}'
            ).setObjectName(f"user_last_message_time_{i}")

            getattr(
                self,
                f'user_last_message_time_{i}'
            ).setHtml(
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                f"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">{last_message.time.strftime('%H:%M') if last_message else ''}</span></p></body></html>")
            # getattr(
            #     self,
            #     f'user_last_message_{i}'
            # ).setText(f"user_last_message_{i}")  # TODO: тут заменить на имя из базы

            """ Фото профиля """

            setattr(
                self, f'user_photo_button_{i}',
                QtWidgets.QLabel(
                    getattr(self, f'user_widget_contents_{i}')
                )
            )  # Добавляем кнопку
            getattr(
                self,
                f'user_photo_button_{i}'
            ).setMaximumSize(40, 40)
            getattr(
                self,
                f'user_photo_button_{i}'
            ).move(5, 20)
            getattr(
                self,
                f'user_photo_button_{i}'
            ).setMinimumSize(40, 40)

            setattr(
                self,
                f'target_{i}',
                QPixmap(getattr(self, f'user_photo_button_{i}').size())
            )
            getattr(self, f'target_{i}').fill(Qt.transparent)

            setattr(
                self,
                f'l_image_{i}',
                QtGui.QPixmap('src/self.jpg').scaled(
                    40, 40, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            )

            setattr(
                self,
                f'painter_{i}',
                QPainter(getattr(self, f'target_{i}'))
            )

            setattr(
                self,
                f'path_{i}',
                QPainterPath()
            )
            getattr(
                self,
                f'path_{i}',
            ).addRoundedRect(
                0, 0, 40, 40, 20, 20)

            getattr(
                self,
                f'painter_{i}'
            ).setClipPath(getattr(self, f'path_{i}'))

            getattr(
                self,
                f'painter_{i}'
            ).drawPixmap(0, 0, getattr(self, f'l_image_{i}'))

            getattr(
                self,
                f'painter_{i}'
            ).end()

            getattr(
                self,
                f'user_photo_button_{i}'
            ).setObjectName(f"user_photo_button_{i}")

            getattr(
                self,
                f'user_photo_button_{i}'
            ).setPixmap(getattr(self, f'target_{i}'))

            """ Экшен кнопка в ней дату хранить будем """
            setattr(
                self, f'user_push_button_{i}',
                QtWidgets.QPushButton(
                    getattr(self, f'user_widget_contents_{i}')
                )
            )  # Добавляем кнопку
            getattr(
                self,
                f'user_push_button_{i}'
            ).setGeometry(QtCore.QRect(0, 0, 259, int(user_high)))
            getattr(
                self,
                f'user_push_button_{i}'
            ).setStyleSheet("color: rgba(255, 255, 255, 0); background-color: rgba(255, 255, 255, 0);")

            getattr(
                self,
                f'user_push_button_{i}'
            ).setObjectName(f"user_push_button_{i}")
            getattr(
                self,
                f'user_push_button_{i}'
            ).setText(str({'chat': chat.chat_id, 'i': i}))  # TODO: тут заменить на имя из базы

        self.scroll_users_area.setWidget(self.scroll_users_area_widget_contents)
        if create:
            self.scroll_users_area.show()
            self.add_users_chat_list_action()

    def retranslateUi(self, chat):
        pass

    def strim(self, str):
        if len(str) > 12:
            str = str[:12] + '...'
        return str


class Chat(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chat, self).__init__()
        self.ui = Ui_chat(self)
        self.init_UI()

    def init_UI(self):
        self.ui.line_write_text.returnPressed.connect(self.send_message)
        self.ui.send_button.clicked.connect(self.send_message)
        self.ui.button_add.clicked.connect(self.add_people)
        self.ui.line_search.returnPressed.connect(self.search_chats)
        self.ui.search_button.clicked.connect(self.search_message)
        self.ui.call_button.clicked.connect(self.call_peer)
        self.ui.more_button.clicked.connect(self.more_functions)
        self.ui.file_button.clicked.connect(self.add_file)
        self.ui.emoji_button.clicked.connect(self.add_emoji)

    def send_message(self):
        if self.ui.chat_id is None:
            return self.make_window(text='Выберите чат')
        text = self.ui.line_write_text.text()
        if len(text) == 0:
            return
        self.ui.line_write_text.clear()
        chat = get(myChat, chat_id=self.ui.chat_id)
        message = sm(chat, text)
        self.ui.scroll_for_message.deleteLater()
        # child = self.ui.scroll_users_area.children()
        # for ch in child:
        #     ch.deleteLater()
        # self.ui.scroll_users_area.deleteLater()
        getattr(
            self.ui,
            f'user_last_message_{self.ui.chat_i}'
        ).setHtml(
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">{self.ui.strim(message.body)}</span></p></body></html>"
        )
        getattr(
            self.ui,
            f'user_last_message_time_{self.ui.chat_i}'
        ).setHtml(
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                f"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">{message.time.strftime('%H:%M')}</span></p></body></html>"
        )

        self.ui.auto_size_message(create=True)
        # self.ui.users_chat_list(create=True)

    def add_people(self):
        self.newWindow = newWindow()
        self.newWindow.show()

    def search_chats(self):
        text = self.ui.line_search.text()
        self.ui.line_search.clear()
        self.make_window()

    def add_emoji(self):
        self.make_window()

    def add_file(self):
        self.make_window()

    def search_message(self):
        self.make_window()

    def call_peer(self):
        self.make_window()

    def more_functions(self):
        self.make_window()

    def make_window(self, text='Скоро будет работать'):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Уведомление")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()


# app = QtWidgets.QApplication([])
# application = Chat()
# application.show()
#
# sys.exit(app.exec())
