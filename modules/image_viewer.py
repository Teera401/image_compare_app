import csv
import os
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
import yaml

from modules.zoomable_view import ZoomableImageView

    
CONFIG_FILE = "config.yaml"
class ImageCompareViewer(QWidget):
    def __init__(self, dir_a="C:\\Users\\tdc123admin\\Tools\\image_compare_app\\images_a", dir_b="C:\\Users\\tdc123admin\\Tools\\image_compare_app\\images_b"):
        super().__init__()

        self.language_mapping_dict = dict()
        self.data_mapping_dict = dict()
        self.initialize_data()

        self.dir_a = dir_a
        self.dir_b = dir_b

        self.images_a = sorted(os.listdir(dir_a))
        self.images_b = sorted(os.listdir(dir_b))
        self.index = 0

        self.init_ui()
        self.load_images()
        
    def initialize_data(self):    
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self.uiCheck_refer_path = config.get("uiCheck_refer_path")
            self.photo_evidence_path = config.get("photo_evidence_path")
            self.photo_evidence_directory = config.get("photo_evidence_directory")
            self.language_all_testcase_path = config.get("language_all_testcase_path")
            pass

    def read_language_mapping(self):
        with open("conf\language_mapping.csv", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)            
            header = next(reader)  # skip header
            for row in reader:
                self.language_mapping_dict[row[0]] = row[1]

    def write_language_name_toconfig(self):
        language_all_testcase = {
            name.split(".")[0] for name in os.listdir(self.language_all_testcase_path)
            if os.path.isdir(os.path.join(self.language_all_testcase_path, name))
        }
        language_all_testcase = sorted(language_all_testcase)

        folders_lang_refer = [
            name for name in os.listdir(self.uiCheck_refer_path)
            if os.path.isdir(os.path.join(self.uiCheck_refer_path, name)) and not name.startswith("_")
        ]

        with open("conf\language_mapping.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Test-Case", "language"])
            lang_idx = 0
            for tc in language_all_testcase:
                writer.writerow([tc, folders_lang_refer[lang_idx] if lang_idx < len(folders_lang_refer) else ""])
                lang_idx += 1

    def init_ui(self):
        self.setWindowTitle("Image Compare (Zoom & Pan)")
        self.resize(1200, 600)

        # Zoomable views
        self.view_a = ZoomableImageView()
        self.view_b = ZoomableImageView()

        # Buttons
        self.back_btn = QPushButton("◀ Back")
        self.next_btn = QPushButton("Next ▶")

        self.back_btn.clicked.connect(self.prev_image)
        self.next_btn.clicked.connect(self.next_image)

        # Layouts
        img_layout = QHBoxLayout()
        img_layout.addWidget(self.view_a)
        img_layout.addWidget(self.view_b)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(img_layout)
        main_layout.addLayout(btn_layout)

    def load_images(self):
        if not self.images_a:
            return

        path_a = os.path.join(self.dir_a, self.images_a[self.index])
        path_b = os.path.join(self.dir_b, self.images_b[self.index])

        self.view_a.set_image(path_a)
        self.view_b.set_image(path_b)

    def next_image(self):
        if self.index < len(self.images_a) - 1:
            self.index += 1
            self.load_images()

    def prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.load_images()

