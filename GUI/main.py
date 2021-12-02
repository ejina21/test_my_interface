from PyQt5 import QtCore, QtGui, QtWidgets

from parent_ui import Ui_chat, Chat

if __name__ == "__main__":
    from multiprocessing import Queue
    from asyncio import Queue as aQueue

    queue_from_ui = aQueue()
    queue_from_core = Queue()

    import sys

    app = QtWidgets.QApplication(sys.argv)
    application = Chat()
    application.show()

    # app = QtWidgets.QApplication(sys.argv)
    # chat = QtWidgets.QMainWindow()
    # ui = Ui_chat(chat, queue_from_ui=queue_from_ui, queue_from_core=queue_from_core)
    # ui.setupUi(chat)
    # chat.show()
    sys.exit(app.exec_())
