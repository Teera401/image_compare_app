
import re

import yaml
import csv
import os

CONFIG_FILE = "config.yaml"
class SettingCnfProvider:
    def __init__(self):
        self.language_mapping_dict = dict()
        self.data_mapping_dict = dict()
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self.uiCheck_refer_path = config.get("uiCheck_refer_path")
            self.photo_evidence_path = config.get("photo_evidence_path")
            self.photo_evidence_directory = config.get("photo_evidence_directory")
            self.language_all_testcase_path = config.get("language_all_testcase_path")
    
    def read_language_mapping(self):
        with open(os.path.join("conf", "language_mapping.csv"), newline="", encoding="utf-8") as file:
            reader = csv.reader(file)            
            header = next(reader)  # skip header
            for row in reader:
                self.language_mapping_dict[row[0]] = row[1]

    def write_language_mapping_config(self):
        language_all_testcase = {
            name.split(".")[0] for name in os.listdir(self.language_all_testcase_path)
            if os.path.isdir(os.path.join(self.language_all_testcase_path, name))
        }
        language_all_testcase = sorted(language_all_testcase)

        folders_lang_refer = [
            name for name in os.listdir(self.uiCheck_refer_path)
            if os.path.isdir(os.path.join(self.uiCheck_refer_path, name)) and not name.startswith("_")
        ]

        with open(os.path.join("conf", "language_mapping.csv"), mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Test-Case", "language"])
            lang_idx = 0
            for tc in language_all_testcase:
                writer.writerow([tc, folders_lang_refer[lang_idx] if lang_idx < len(folders_lang_refer) else ""])
                lang_idx += 1

    def write_refer_data_mapping_config(self):
        files_lang_refer_pics = list()
        ref_id = 0
        for lang in os.listdir(self.uiCheck_refer_path):
            lang_path = os.path.join(self.uiCheck_refer_path, lang)
            if os.path.isdir(lang_path):
                for pic_name in os.listdir(lang_path):
                    full_path = os.path.join(lang_path, pic_name)
                    if os.path.isfile(full_path):
                        files_lang_refer_pics.append(PicProp(ref_id,lang, pic_name, full_path))
                        ref_id = ref_id + 1
        with open(os.path.join("conf", "pic_mapping.csv"), mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Reference ID", "Language", "Pic Map Name", "Full Path", "Hash Value"])            
            for pic in files_lang_refer_pics:
                pic: PicProp
                writer.writerow([pic.ref_id, pic.language, pic.pic_map_name, pic.full_path, pic.hash_value])

    def read_refer_data_mapping_config(self):
        with open(os.path.join("conf", "pic_mapping.csv"), newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)            
            for row in reader:
                self.data_mapping_dict[row["Reference ID"]] = {
                    "language": row["Language"],
                    "pic_map_name": row["Pic Map Name"],
                    "full_path": row["Full Path"],
                    "hash_value": row["Hash Value"]
                }   

                
class PicProp:
    def __init__(self, ref_id=None, language=None, pic_name=None, full_path=None):
        self.ref_id = ref_id
        self.language = language
        self.pic_map_name = re.sub(r'[^a-zA-Z0-9_,]', '', (pic_name.split(".")[0])) if pic_name else None
        self.full_path = full_path
        self.hash_value = self.__calculate_hash() if full_path else None

    def __calculate_hash(self):
        import hashlib
        hash_md5 = hashlib.md5()
        with open(self.full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

        