from PyQt5 import QtCore, QtWidgets

from test_my_interface.GUI.db.db_utils import get_or_create_user, get_or_create_chat


class newWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.data = [{'external_uuid': 'a621ac24-1a56-4881-be01-b65454e4670d', 'FIO': 'stas', 'nickname': 'stas'},
                    {'external_uuid': 'fd3ff11a-7bdd-476b-a6f5-332aac5ae517', 'FIO': 'maks', 'nickname': 'maks'}]

            # data = requests.get('http://18.224.57.255:8000/client/api/agents/').json()
        except Exception as e:
            self.data = []
            print("Error requests agents")
            print(e)
        print(f'{self.data=}')
        self.top = 0
        self.left = 0
        self.width = 300
        self.height = 300
        self.setMinimumSize(QtCore.QSize(300, 300))
        self.setMaximumSize(QtCore.QSize(300, 300))
        self.setWindowTitle('Добавить чат')
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.scroll_u_area = QtWidgets.QScrollArea(self)
        self.scroll_u_area.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.scroll_u_area.setObjectName("scroll_u_area")
        self.scroll_u_area.setStyleSheet("border: none; background-color: #EFFFEF;")
        self.scroll_u_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.widget = QtWidgets.QWidget(self.scroll_u_area)
        self.widget.setGeometry(QtCore.QRect(0, 0, self.width, 50 * len(self.data)))
        self.widget.setStyleSheet("background-color: #EFFFEF;")
        self.widget.setObjectName("widget")

        for i in range(len(self.data)):
            setattr(
                self,
                f'u_button_{i}',
                QtWidgets.QPushButton(self.widget)
            )
            getattr(
                self,
                f'u_button_{i}'
            ).setGeometry(QtCore.QRect(10, 10 + 45 * i, 280, 40))

            getattr(
                self,
                f'u_button_{i}'
            ).setStyleSheet("background-color: rgb(153, 153, 153);")
            getattr(
                self,
                f'u_button_{i}'
            ).setText(f"{self.data[i]['nickname']} - {self.data[i]['FIO']}")
            getattr(
                self,
                f'u_button_{i}'
            ).setObjectName(f'u_button_{i}')

        self.click()

    def click(self):
        i = 0
        while getattr(self, f'u_button_{i}', None):
            getattr(
                self,
                f'u_button_{i}'
            ).clicked.connect(self.add)
            i += 1

    def add(self):
        obj = self.sender()
        name = obj.text().split(' - ')
        nick = name[0]
        for dict in self.data:
            if dict.get('nickname') == nick:
                user = get_or_create_user(username=nick, first_name=dict.get('FIO'), last_name=dict.get('FIO'),)
                get_or_create_chat(user)
                break
        obj.deleteLater()
