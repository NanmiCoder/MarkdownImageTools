import os

import markdown
from pygments.formatters import HtmlFormatter
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QFileDialog,
                             QHBoxLayout, QLabel, QMainWindow, QMessageBox,
                             QProgressBar, QPushButton, QTextBrowser,
                             QVBoxLayout, QWidget, QLineEdit)

from config import IMAGE_PROVIDER_NAME
from core.file_handler import FileHandler
from core.image_uploader import ImageUploader
from core.markdown_parser import MarkdownParser
from utils.config import load_style_sheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Image Replacer")
        self.resize(800, 600)
        self.setStyleSheet(load_style_sheet())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()

        self.markdown_parser = MarkdownParser()
        self.image_uploader = ImageUploader(upload_service=IMAGE_PROVIDER_NAME)
        self.file_handler = FileHandler()

        self.markdown_content = ""
        self.base_path = ""
        self.total_images = 0
        self.processed_images = 0

        self.center_window()

    def center_window(self):
        """
        Centers the window on the screen.
        :return:
        """
        screen = QDesktopWidget().screenNumber(QDesktopWidget().cursor().pos())
        center_point = QDesktopWidget().screenGeometry(screen).center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def setup_ui(self):
        """
        Sets up the UI components.
        :return:
        """
        # 创建一个水平布局来放置输入框和按钮
        input_layout = QHBoxLayout()

        # 添加一个 QLineEdit 来输入文件路径
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("输入Markdown文件的绝对文件地址")
        self.path_input.setMinimumHeight(45)  # 设置最小高度        
        input_layout.addWidget(self.path_input)

        # 添加一个按钮用于从文件对话框选择文件
        self.browse_button = QPushButton("选择电脑中的Markdown文件")
        self.browse_button.clicked.connect(self.browse_file)
        self.browse_button.setMinimumHeight(30)
        input_layout.addWidget(self.browse_button)

        # 添加一个按钮用于加载输入框中的路径
        self.load_button = QPushButton("加载文件")
        self.load_button.clicked.connect(self.load_markdown_from_path)
        self.load_button.setMinimumHeight(30)
        input_layout.addWidget(self.load_button)

        # 将水平布局添加到主布局中
        self.layout.addLayout(input_layout)

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        font = QFont("Courier")
        font.setPointSize(12)
        self.text_browser.setFont(font)
        self.layout.addWidget(self.text_browser)

        progress_layout = QHBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)  # 设置初始范围为0-100
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # 隐藏进度条上的文字
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("没有图片在处理中")
        progress_layout.addWidget(self.progress_label)

        self.layout.addLayout(progress_layout)

        self.replace_button = QPushButton("替换Markdown中图片")
        self.replace_button.clicked.connect(self.replace_images)
        self.replace_button.setEnabled(False)
        self.layout.addWidget(self.replace_button)

        self.download_button = QPushButton("下载修改后的Markdown文件")
        self.download_button.clicked.connect(self.download_markdown)
        self.download_button.setEnabled(False)
        self.layout.addWidget(self.download_button)

    def browse_file(self):
        """
        Opens a file dialog to select a Markdown file and sets the path in the QLineEdit.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Markdown文件", "", "Markdown Files (*.md)")
        if file_path:
            self.path_input.setText(file_path)  # 将选择的文件路径设置到输入框中

    def load_markdown_from_path(self):
        """
        Loads the Markdown file from the path specified in the QLineEdit.
        :return:
        """
        file_path = self.path_input.text().strip()
        if file_path:
            self.process_markdown_file(file_path)
        else:
            QMessageBox.warning(self, "错误", "请输入一个有效的文件路径.")

    def process_markdown_file(self, file_path):
        """
        Processes the Markdown file at the given path.
        :param file_path: str
        :return:
        """
        self.markdown_content = self.file_handler.read_file(file_path)
        self.base_path = os.path.dirname(file_path)
        self.markdown_content = self.markdown_parser.replace_image_paths(self.markdown_content, self.base_path)

        # 计算总图片数量
        images = self.markdown_parser.parse_images(self.markdown_content)
        self.total_images = len(images)
        self.processed_images = 0

        # 更新进度条和标签
        if self.total_images > 0:
            self.progress_bar.setRange(0, self.total_images)
            self.progress_bar.setValue(0)
            self.progress_label.setText(f"0 / {self.total_images}")
            self.replace_button.setEnabled(True)
        else:
            self.progress_bar.setRange(0, 1)  # 设置范围为0-1
            self.progress_bar.setValue(1)  # 设置值为1，显示满格
            self.progress_label.setText("No images to process")
            self.replace_button.setEnabled(False)

        self.render_markdown(self.markdown_content)
        self.download_button.setEnabled(False)

    def replace_images(self):
        """
        Replaces the images in the Markdown file.
        :return:
        """
        if self.total_images == 0:
            QMessageBox.information(self, "No Images", "There are no images to process in this Markdown file.")
            return

        self.browse_button.setEnabled(False)
        self.replace_button.setEnabled(False)

        images = self.markdown_parser.parse_images(self.markdown_content)
        for i, image in enumerate(images):
            image_path = image['path']
            if not image_path.startswith(('http://', 'https://')):
                full_path = os.path.join(self.base_path, image_path)
                if os.path.exists(full_path):
                    try:
                        new_url = self.image_uploader.upload(full_path)
                        new_image_markdown = f'![{image["alt_text"]}]({new_url})'
                        self.markdown_content = self.markdown_content.replace(image['original'], new_image_markdown)
                    except Exception as e:
                        QMessageBox.warning(self, "Upload Error", f"Failed to upload image {image_path}: {str(e)}")
                else:
                    QMessageBox.warning(self, "File Not Found", f"Image file not found: {full_path}")

            self.processed_images += 1
            self.progress_bar.setValue(self.processed_images)
            self.progress_label.setText(f"{self.processed_images} / {self.total_images}")
            QApplication.processEvents()  # 确保 UI 更新

        self.render_markdown(self.markdown_content)
        self.browse_button.setEnabled(True)
        self.replace_button.setEnabled(True)
        self.download_button.setEnabled(True)

    def render_markdown(self, content):
        """
        Renders the Markdown content in the QTextBrowser.
        :param content:
        :return:
        """
        html = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
        formatter = HtmlFormatter(style='colorful')
        css = formatter.get_style_defs('.codehilite')
        html = f'<style>{css}</style>{html}'
        self.text_browser.setHtml(html)

    def download_markdown(self):
        """
        Downloads the modified Markdown file.
        :return:
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Markdown File", "", "Markdown Files (*.md)")
        if file_path:
            self.file_handler.write_file(file_path, self.markdown_content)
            QMessageBox.information(self, "Success", "Markdown file saved successfully.")

