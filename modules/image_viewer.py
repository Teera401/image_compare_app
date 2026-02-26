import csv
import os
from PySide6.QtWidgets import QCheckBox, QLabel, QLineEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
import yaml
from PySide6.QtWidgets import QFileDialog
from modules.pic_prop_evidence import PicPropEvidence
from modules.setting_cnf_provider import SettingCnfProvider
from modules.zoomable_view import ZoomableImageView

    
CONFIG_FILE = "config.yaml"
class ImageCompareViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.settingCnfProvider = SettingCnfProvider()
        # self.evidence_alias_mapping_dict = self.settingCnfProvider.read_evidence_mapping_config(is_from_folder=False)
        # read_evidence_mapping_config = settingCnf.read_evidence_mapping_config()
        self.index = None
        self.init_ui()
        # self.next_image()

    def set_index(self):
        try:
            idx = int(self.txt_set_index.text())
            if 0 <= idx < len(self.evidence_alias_mapping_dict):
                self.index = idx
                self.next_image()
            else:
                self.txt_set_index.setText("")
        except ValueError:
            self.txt_set_index.setText("")

    def init_ui(self):
        self.setWindowTitle("Image Compare (Zoom & Pan)")
        self.resize(1200, 600)

        self.label_index = QLabel()
        self.cb_fixed_picref = QCheckBox("Fixed PicRef")
        self.txt_set_index = QLineEdit()
        
        self.txt_set_index.returnPressed.connect(self.set_index)
        # Zoomable views
        self.view_ref = ZoomableImageView()
        self.view_evidence = ZoomableImageView()

        # Buttons
        self.back_btn = QPushButton("◀ Back")
        self.next_btn = QPushButton("Next ▶")

        self.back_btn.clicked.connect(self.prev_image)
        self.next_btn.clicked.connect(self.next_image)

        # Layouts Label
        label_layout = QHBoxLayout()
        label_ref = QLabel("Reference")
        btn_choot_folder_evd = QPushButton("Choose Evidence Folder")
        btn_choot_folder_evd.clicked.connect(self.choose_evidence_folder)
        label_layout.addWidget(label_ref)
        label_layout.addWidget(btn_choot_folder_evd)

        # Layouts
        txt_path_layout = QHBoxLayout()
        self.tbx_path_ref = QLineEdit()
        self.tbx_path_evidence = QLineEdit()
        txt_path_layout.addWidget(QLabel("Path Ref:"))
        txt_path_layout.addWidget(self.tbx_path_ref)
        txt_path_layout.addWidget(QLabel("Path Evidence:"))
        txt_path_layout.addWidget(self.tbx_path_evidence)

        text_alias_layout = QHBoxLayout()
        self.tbx_alias_ref = QLineEdit()
        self.tbx_alias_evidence = QLineEdit()
        text_alias_layout.addWidget(QLabel("Alias Ref:"))
        text_alias_layout.addWidget(self.tbx_alias_ref)
        text_alias_layout.addWidget(QLabel("Alias Evidence:"))
        text_alias_layout.addWidget(self.tbx_alias_evidence)


        # Layouts
        img_layout = QHBoxLayout()
        img_layout.addWidget(self.view_ref)
        img_layout.addWidget(self.view_evidence)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.txt_set_index)
        btn_layout.addWidget(self.cb_fixed_picref)
        btn_layout.addWidget(self.label_index)
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(label_layout)
        main_layout.addLayout(text_alias_layout)
        main_layout.addLayout(txt_path_layout)
        main_layout.addLayout(img_layout)
        main_layout.addLayout(btn_layout)

    def choose_evidence_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Evidence Folder", "")
        if folder_path:
            self.btn_choot_folder_evd.setEnabled(False)
            self.settingCnfProvider.is_mamual_photo_evidence_path = True
            self.settingCnfProvider.photo_evidence_path = folder_path
            self.evidence_alias_mapping_dict = self.settingCnfProvider.read_evidence_mapping_config(is_from_folder=True)
            self.index = None
        self.btn_choot_folder_evd.setEnabled(True)

    def load_images(self, ref_pic_path=None, evidence_pic_path=None):
        self.view_ref.set_image(ref_pic_path)
        self.view_evidence.set_image(evidence_pic_path)

    def next_image(self):        
        if self.index is None:
            self.index = 0
        elif self.index < len(self.evidence_alias_mapping_dict) - 1:
                self.index += 1
        picPropEvidence:PicPropEvidence = list(self.evidence_alias_mapping_dict.values())[self.index] if self.index < len(self.evidence_alias_mapping_dict) else None
        if not picPropEvidence:
            return
        self.picPropRef = picPropEvidence.PicPropRef if not self.cb_fixed_picref.isChecked() else self.picPropRef 

        self.label_index.setText(f"Index: {self.index} / {len(self.evidence_alias_mapping_dict)-1}")
        ref_pic_path = self.picPropRef.full_path if self.picPropRef else None
        evidence_pic_path = picPropEvidence.full_path if picPropEvidence else None
        self.tbx_path_ref.setText(ref_pic_path if ref_pic_path else "")
        self.tbx_path_evidence.setText(evidence_pic_path if evidence_pic_path else "")
        self.tbx_alias_ref.setText(self.picPropRef.alias if self.picPropRef else "")
        self.tbx_alias_evidence.setText(picPropEvidence.alias if picPropEvidence else "")
        self.load_images(ref_pic_path, evidence_pic_path)


    def prev_image(self):
        if self.index is None:
            self.index = 0
        elif self.index > 0:
                self.index -= 1
        picPropEvidence:PicPropEvidence = list(self.evidence_alias_mapping_dict.values())[self.index] if self.index < len(self.evidence_alias_mapping_dict) else None
        if not picPropEvidence:
            return
        self.picPropRef = picPropEvidence.PicPropRef if not self.cb_fixed_picref.isChecked() else self.picPropRef 
        self.label_index.setText(f"Index: {self.index} / {len(self.evidence_alias_mapping_dict)-1}")
        ref_pic_path = self.picPropRef.full_path if self.picPropRef else None
        evidence_pic_path = picPropEvidence.full_path if picPropEvidence else None
        self.tbx_path_ref.setText(ref_pic_path if ref_pic_path else "")
        self.tbx_path_evidence.setText(evidence_pic_path if evidence_pic_path else "")
        self.tbx_alias_ref.setText(self.picPropRef.alias if self.picPropRef else "")
        self.tbx_alias_evidence.setText(picPropEvidence.alias if picPropEvidence else "")
        self.load_images(ref_pic_path, evidence_pic_path)

