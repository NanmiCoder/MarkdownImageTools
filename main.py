import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

import utils

def main():
    utils.logger.info("Starting Markdown Image Tools")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
