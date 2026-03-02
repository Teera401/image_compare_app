from datetime import datetime
import os
import pandas as pd

from PySide6.QtWidgets import QCheckBox, QLabel, QLayout, QLineEdit, QTextEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPalette, Qt
import yaml
from PySide6.QtWidgets import QFileDialog
from modules.pic_prop_evidence import PicPropEvidence
from modules.setting_cnf_provider import SettingCnfProvider
from modules.zoomable_view import ZoomableImageView

    
CONFIG_FILE = "config.yaml"
SHEET_HEAD = 'Head-New'
SHEET_PARA = 'Para-New'

class ImageCompareViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.settingCnfProvider = SettingCnfProvider()
        self.evidence_alias_mapping_dict = dict()
        # self.evidence_alias_mapping_dict = self.settingCnfProvider.read_evidence_mapping_config(is_from_folder=False)
        # read_evidence_mapping_config = settingCnf.read_evidence_mapping_config()
        self.index = None
        self.init_ui()
        
        self.header_string_lang_dict = dict()
        self.para_string_lang_dict = dict()
        # self.load_string_language_xls(self.settingCnfProvider.text_string_compare_file)

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
    def clear_all_components_value(self):
        self.txt_set_index.setText("")
        self.tbx_path_ref.setText("")
        self.tbx_path_evidence.setText("")
        self.tbx_alias_ref.setText("")
        self.tbx_alias_evidence.setText("")
        self.picture_number.setText(f"Index: - / {len(self.evidence_alias_mapping_dict)}")
        self.view_ref.set_image(None)
        self.view_evidence.set_image(None)
        self.tbx_head_bx2_ch1.setText("")
        self.tbx_para_bx2_ch2.setText("")

    def init_ui(self):
        self.setWindowTitle("Image Compare (Zoom & Pan)")
        self.resize(1200, 600)

        self.picture_number = QLabel()
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
        self.back_btn.setFixedHeight(40)
        self.next_btn.setFixedHeight(40)
        self.back_btn.setFixedWidth(100)
        self.next_btn.setFixedWidth(100)
        self.back_btn.setStyleSheet("background-color: lightblue;")
        self.next_btn.setStyleSheet("background-color: lightblue;")

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
        text_alias_layout.addStretch()
  
        img_layout = QHBoxLayout()
        img_layout.addWidget(self.view_ref)
        img_layout.addWidget(self.view_evidence)




        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        # btn_layout.setAlignment(Qt.AlignBottom)
        # btn_layout.addWidget(self.txt_set_index)
        # btn_layout.addWidget(self.cb_fixed_picref)
        btn_layout.addWidget(self.picture_number)
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addStretch()


        label_ref_txt = QLabel("Referent Text String:")
        self.label_xlsx_file_ver = QLabel("Version Date: ---")
        self.ref_txt_xlsx_file = QLineEdit()
        self.ref_txt_xlsx_file.setFixedWidth(300)
        self.ref_txt_xlsx_file.setFixedHeight(40)  
        self.ref_txt_xlsx_file.setReadOnly(True)
        self.ref_choose_btn = QPushButton("Choose XLSX File")
        self.ref_choose_btn.setStyleSheet("background-color: lightgreen;")
        self.ref_choose_btn.setFixedWidth(150)
        self.ref_choose_btn.setFixedHeight(40)
        lang_xlsx_layout_bx1_ch1 = QHBoxLayout()
        self.ref_choose_btn.clicked.connect(self.choose_ref_text_xlsx_file)
        lang_xlsx_layout_bx1_ch1.addWidget(label_ref_txt, alignment=Qt.AlignLeft)
        lang_xlsx_layout_bx1_ch1.addWidget(self.ref_txt_xlsx_file, alignment=Qt.AlignLeft)
        lang_xlsx_layout_bx1_ch1.addWidget(self.ref_choose_btn, alignment=Qt.AlignLeft)
        lang_xlsx_layout_bx1_ch1.addStretch()
        box1_layout = QVBoxLayout()
        box1_layout.addLayout(lang_xlsx_layout_bx1_ch1)
        box1_layout.addWidget(self.label_xlsx_file_ver)
        # box1_layout.addStretch()

        label_head_bx2_ch1 = QLabel("Heading:")
        self.tbx_head_bx2_ch1 = QTextEdit()
        self.tbx_head_bx2_ch1.setReadOnly(True)
        self.tbx_head_bx2_ch1.setFixedWidth(350)
        self.tbx_head_bx2_ch1.setFixedHeight(40)
        label_para_bx2_ch2 = QLabel("Paragraph:")
        self.tbx_para_bx2_ch2 = QTextEdit()
        self.tbx_para_bx2_ch2.setReadOnly(True)
        self.tbx_para_bx2_ch2.setFixedWidth(350)
        self.tbx_para_bx2_ch2.setFixedHeight(70)
        lang_xlsx_layout_bx2_ch1 = QHBoxLayout()
        lang_xlsx_layout_bx2_ch1.addWidget(label_head_bx2_ch1, alignment=Qt.AlignLeft)
        lang_xlsx_layout_bx2_ch1.addWidget(self.tbx_head_bx2_ch1, alignment=Qt.AlignRight)
        lang_xlsx_layout_bx2_ch1.addStretch()
        lang_xlsx_layout_bx2_ch2 = QHBoxLayout()
        lang_xlsx_layout_bx2_ch2.addWidget(label_para_bx2_ch2, alignment=Qt.AlignLeft)
        lang_xlsx_layout_bx2_ch2.addWidget(self.tbx_para_bx2_ch2, alignment=Qt.AlignRight)
        lang_xlsx_layout_bx2_ch2.addStretch()
        box2_layout = QVBoxLayout()
        box2_layout.addLayout(lang_xlsx_layout_bx2_ch1)
        box2_layout.addLayout(lang_xlsx_layout_bx2_ch2)
        # box2_layout.addStretch()


                # Layouts Label
        eviden_resource_layout = QHBoxLayout()
        label_ref = QLabel("Reference")
        self.btn_choot_folder_evd = QPushButton("Choose Evidence Folder")
        self.btn_choot_folder_evd.setFixedHeight(40)
        self.btn_choot_folder_evd.setFixedWidth(150)
        self.btn_choot_folder_evd.setStyleSheet("background-color: lightgreen;")
        self.btn_choot_folder_evd.clicked.connect(self.choose_evidence_folder)
        self.evidence_select_path = QLineEdit()
        self.evidence_select_path.setReadOnly(True)
        self.evidence_select_path.setFixedHeight(40)
        self.evidence_select_path.setFixedWidth(250)
        eviden_resource_layout.addWidget(label_ref)
        eviden_resource_layout.addWidget(self.evidence_select_path)
        eviden_resource_layout.addWidget(self.btn_choot_folder_evd)
        eviden_resource_layout.addStretch()

        pass_fail_layout = QHBoxLayout()
        fail_btn = QPushButton("Fail")
        fail_btn.setStyleSheet("background-color: gray; color: white;")
        fail_btn.setFixedWidth(125)
        fail_btn.setFixedHeight(50)
        pass_btn = QPushButton("Pass")
        pass_btn.setStyleSheet("background-color: gray; color: white;")
        pass_btn.setFixedWidth(125)
        pass_btn.setFixedHeight(50)
        pass_fail_layout.addWidget(fail_btn)
        pass_fail_layout.addWidget(pass_btn)
        pass_fail_layout.addStretch()

        box3_layout = QVBoxLayout()
        box3_layout.setAlignment(Qt.AlignBottom)
        box3_layout.addLayout(eviden_resource_layout)
        box3_layout.addLayout(pass_fail_layout)
        # box3_layout.addStretch()

        buttom_layout_base_0 = QHBoxLayout()
        buttom_layout_base_0.setAlignment(Qt.AlignBottom)
        buttom_layout_base_0.addLayout(box1_layout)
        buttom_layout_base_0.addLayout(box2_layout)
        buttom_layout_base_0.addLayout(box3_layout)
        buttom_layout_base_0.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(text_alias_layout)
        main_layout.addLayout(txt_path_layout)
        main_layout.addLayout(img_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(buttom_layout_base_0)

    def choose_ref_text_xlsx_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select XLSX File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.load_string_language_xls(file_path)

    def choose_evidence_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Evidence Folder", "")
        if folder_path:
            self.btn_choot_folder_evd.setText("Loading...")
            self.btn_choot_folder_evd.setEnabled(False)
            self.settingCnfProvider.is_mamual_photo_evidence_path = True
            self.settingCnfProvider.photo_evidence_path = folder_path
            self.evidence_alias_mapping_dict = self.settingCnfProvider.read_evidence_mapping_config(is_from_folder=True)
            self.index = None
            self.evidence_select_path.setText(folder_path)
        self.btn_choot_folder_evd.setText("Choose Evidence Folder")
        self.btn_choot_folder_evd.setEnabled(True)
        self.clear_all_components_value()


    def load_images(self, ref_pic_path=None, evidence_pic_path=None):
        self.view_ref.set_image(ref_pic_path)
        self.view_evidence.set_image(evidence_pic_path)

    def next_image(self):    
        self.tbx_head_bx2_ch1.setText("")
        self.tbx_para_bx2_ch2.setText("")    
        if self.index is None:
            self.index = 0
        elif self.index < len(self.evidence_alias_mapping_dict) - 1:
                self.index += 1
        picPropEvidence:PicPropEvidence = list(self.evidence_alias_mapping_dict.values())[self.index] if self.index < len(self.evidence_alias_mapping_dict) else None
        if not picPropEvidence:
            return
        self.picPropRef = picPropEvidence.PicPropRef if not self.cb_fixed_picref.isChecked() else self.picPropRef
        self.picture_number.setText(f"Pic Number: {self.index + 1} / {len(self.evidence_alias_mapping_dict)}")
        ref_pic_path = self.picPropRef.full_path if self.picPropRef else None
        evidence_pic_path = picPropEvidence.full_path if picPropEvidence else None
        self.tbx_path_ref.setText(ref_pic_path if ref_pic_path else "")
        self.tbx_path_evidence.setText(evidence_pic_path if evidence_pic_path else "")
        self.tbx_alias_ref.setText(self.picPropRef.alias if self.picPropRef else "")
        self.tbx_alias_evidence.setText(picPropEvidence.alias if picPropEvidence else "")

        self.load_images(ref_pic_path, evidence_pic_path)
        
        string_head_dict:dict = self.header_string_lang_dict.get(self.picPropRef.pic_name_without_exten) if self.picPropRef else None
        if string_head_dict:
            head_string = string_head_dict.get(self.picPropRef.language)
            self.tbx_head_bx2_ch1.setText(head_string)
        string_para_dict:dict = self.para_string_lang_dict.get(self.picPropRef.pic_name_without_exten) if self.picPropRef else None
        if string_para_dict:
            para_string = string_para_dict.get(self.picPropRef.language)
            self.tbx_para_bx2_ch2.setText(para_string)

    def prev_image(self):
        self.tbx_head_bx2_ch1.setText("")
        self.tbx_para_bx2_ch2.setText("")
        if self.index is None:
            self.index = 0
        elif self.index > 0:
                self.index -= 1
        picPropEvidence:PicPropEvidence = list(self.evidence_alias_mapping_dict.values())[self.index] if self.index < len(self.evidence_alias_mapping_dict) else None
        if not picPropEvidence:
            return
        self.picPropRef = picPropEvidence.PicPropRef if not self.cb_fixed_picref.isChecked() else self.picPropRef 
        self.picture_number.setText(f"Pic Number: {self.index + 1} / {len(self.evidence_alias_mapping_dict)}")
        ref_pic_path = self.picPropRef.full_path if self.picPropRef else None
        evidence_pic_path = picPropEvidence.full_path if picPropEvidence else None
        self.tbx_path_ref.setText(ref_pic_path if ref_pic_path else "")
        self.tbx_path_evidence.setText(evidence_pic_path if evidence_pic_path else "")
        self.tbx_alias_ref.setText(self.picPropRef.alias if self.picPropRef else "")
        self.tbx_alias_evidence.setText(picPropEvidence.alias if picPropEvidence else "")
        self.load_images(ref_pic_path, evidence_pic_path)
        string_head_dict:dict = self.header_string_lang_dict.get(self.picPropRef.pic_name_without_exten) if self.picPropRef else None
        if string_head_dict:
            head_string = string_head_dict.get(self.picPropRef.language)
            self.tbx_head_bx2_ch1.setText(head_string)
        string_para_dict:dict = self.para_string_lang_dict.get(self.picPropRef.pic_name_without_exten) if self.picPropRef else None
        if string_para_dict:
            para_string = string_para_dict.get(self.picPropRef.language)
            self.tbx_para_bx2_ch2.setText(para_string)


    
    def load_string_language_xls(self, file_path):   
        self.ref_choose_btn.setEnabled = False 
        self.ref_choose_btn.setText("Loading...")  
        timestamp = os.path.getmtime(file_path)
        modified_date = datetime.fromtimestamp(timestamp) 
        self.label_xlsx_file_ver.setText(f"Version Date: {modified_date}")
        df_head = pd.read_excel(file_path, sheet_name=SHEET_HEAD)
        df_para = pd.read_excel(file_path, sheet_name=SHEET_PARA)
        
        def __read_data(df, target_dict):
            col_index_dict = dict()    
            for index, row in df.iterrows():
                if index == 0:
                    for col_idx, col in enumerate(df.columns):
                        col_index_dict[col_idx] = col
                elif index > 0:
                    # text_string_compare = StringCompareSlsx()
                    image_ref_name = ""
                    for col_idx, cell_value in enumerate(row):
                        if col_idx == 0:
                            image_ref_name = str(cell_value).split(".")[0] if pd.notna(cell_value) else ""
                            if image_ref_name not in target_dict:
                                target_dict[image_ref_name] = dict()
                            continue
                        language = col_index_dict.get(col_idx, f"Language_{col_idx}")
                        target_dict[image_ref_name][language] = cell_value                    
        __read_data(df_head, self.header_string_lang_dict)
        __read_data(df_para, self.para_string_lang_dict)

        self.ref_txt_xlsx_file.setText(os.path.basename(file_path) if file_path else None)
        self.ref_choose_btn.setEnabled = True
        self.ref_choose_btn.setText("Choose XLSX File")
        return 

