
import re

from trio import Path
import yaml
import csv
import os

from modules.pic_prop_evidence import PicPropEvidence
from modules.pic_prop_ref import PicPropRef
from modules.text_string_compare import TextStringCompare

CONFIG_FILE = "config.yaml"
IMAGE_EXTS = (".jpg", ".jpeg", ".png")

class SettingCnfProvider:
    def __init__(self):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self.uiCheck_refer_path = config.get("uiCheck_refer_path")
            self.photo_evidence_path = config.get("photo_evidence_path")
            self.photo_evidence_directory = config.get("photo_evidence_directory")
            self.language_all_testcase_path = config.get("language_all_testcase_path")
            self.text_string_compare_file = config.get("text_string_compare_file")
            self.is_mamual_photo_evidence_path = False

            
    
    def read_language_mapping(self):
        language_mapping_dict = dict()
        with open(os.path.join("conf", "language_mapping.csv"), newline="", encoding="utf-8") as file:
            reader = csv.reader(file)            
            header = next(reader)  # skip header
            for row in reader:
                language_mapping_dict[row[0]] = row[1]
        return language_mapping_dict    
            

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
        # ref_lang_id = 0
        for lang in os.listdir(self.uiCheck_refer_path):
            lang_path = os.path.join(self.uiCheck_refer_path, lang)
            # ref_lang_id = ref_lang_id + 1000
            if os.path.isdir(lang_path):
                # pic_id = 0
                for pic_name in os.listdir(lang_path):
                    full_path = os.path.join(lang_path, pic_name)
                    if os.path.isfile(full_path):                        
                        # ref_id = ref_lang_id + pic_id
                        files_lang_refer_pics.append(PicPropRef( lang, pic_name, full_path))
                        # pic_id += 1
        with open(os.path.join("conf", "ref_pic_mapping.csv"), mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([ "Language", "Alias", "Full Path", "Hash Value"])            
            for pic in files_lang_refer_pics:
                pic: PicPropRef
                writer.writerow([pic.language, pic.alias, pic.full_path, pic.hash_value])

    def read_refer_data_mapping_config(self):
        data_mapping_list = list()
        with open(os.path.join("conf", "ref_pic_mapping.csv"), newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)            
            for row in reader:
                picPropRefObj = PicPropRef(language=row["Language"], alias=row["Alias"], full_path=row["Full Path"])
                data_mapping_list.append(picPropRefObj)
                # data_mapping_list.append({
                #     # "reference_id": row["Reference ID"],
                #     "language": row["Language"],
                #     "alias": row["Alias"],
                #     "full_path": row["Full Path"],
                #     "hash_value": row["Hash Value"]
                # })
        return data_mapping_list

    def get_pic_prop_evidence(self):
        evidence_pics = []
        level = 0
        for root, dirs, files in os.walk(self.photo_evidence_path):
            if not self.is_mamual_photo_evidence_path:
                dirs[:] = [d for d in dirs if d.startswith("VTP")] if level == 0 else dirs
            for file in files:
                if file.lower().endswith(IMAGE_EXTS):
                    full_path = os.path.join(root, file)
                    evidence_pics.append(PicPropEvidence(full_path))
            level += 1
        return evidence_pics

    def write_evidence_mapping_config(self):
        evidence_pics = self.get_pic_prop_evidence()        
        with open(os.path.join("conf", "evidence_pic_mapping.csv"), mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Alias", "VTP Name", "Full Path"])
            for pic in evidence_pics:
                pic: PicPropEvidence
                writer.writerow([pic.alias, pic.vpt_name, pic.full_path])

    def read_alias_evidence_alias_mapping_config(self):
        evidence_alias_mapping_set = set()
        with open(os.path.join("conf", "evidence_pic_mapping.csv"), newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)            
            for row in reader:
                evidence_alias_mapping_set.add(row["Alias"])
        evidence_alias_mapping_set = sorted(evidence_alias_mapping_set)
        return evidence_alias_mapping_set  

# Initial Data  
    def read_evidence_mapping_config(self, is_from_folder=False):
        alias_mapping_config_dict = self.read_alias_mapping_config()  #adjustcontactl,r,t,  adjust_contact_1
        refer_data_mapping_list = self.read_refer_data_mapping_config()
        language_mapping = self.read_language_mapping()
        evidence_alias_mapping_dict = dict()
        if not is_from_folder:
            with open(os.path.join("conf", "evidence_pic_mapping.csv"), newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)            
                for row in reader:
                    picPropEvidence = PicPropEvidence(full_path=row["Full Path"])
                    picPropEvidence.set_picprop_ref(alias_mapping_config_dict, refer_data_mapping_list, language_mapping)
                    evidence_alias_mapping_dict[picPropEvidence.key] = picPropEvidence
        else:
            evidence_pics = self.get_pic_prop_evidence()
            for pic in evidence_pics:
                pic: PicPropEvidence
                pic.set_picprop_ref(alias_mapping_config_dict, refer_data_mapping_list, language_mapping)
                evidence_alias_mapping_dict[pic.key] = pic

        evidence_alias_mapping_dict = dict(sorted(evidence_alias_mapping_dict.items(), key=lambda item: item[0]))
        return evidence_alias_mapping_dict  
    
    def read_text_string_compare_data(self):
        text_string_compare_data = TextStringCompare.load_data_xls(self.text_string_compare_file)
        return text_string_compare_data
    
    

    def write_alias_mapping_config(self):
        data_mapping_list = self.read_refer_data_mapping_config()
        refprop = set()
        for data in data_mapping_list:
            data: PicPropRef
            refprop.add(data.alias)
        refprop = sorted(refprop)
        evidence_alias_mapping_set = self.read_alias_evidence_alias_mapping_config()

        with open(os.path.join("conf", "alias_mapping.csv"), mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Ref Alias", "Evidence Alias", "Evidence Alias 2", "Evidence Alias 3"])
            indx = 0

            for alias in refprop:    
                writer.writerow([alias, evidence_alias_mapping_set[indx] if indx < len(evidence_alias_mapping_set) else "", "", ""])
                indx += 1
            if indx < len(evidence_alias_mapping_set):
                for i in range(indx, len(evidence_alias_mapping_set)):
                    writer.writerow(["", evidence_alias_mapping_set[i], "", ""])

    def read_alias_mapping_config(self):
        alias_mapping_dict = dict()
        with open(os.path.join("conf", "alias_mapping.csv"), newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)            
            for row in reader:
                alias_mapping_dict[row["Ref Alias"]] = [row["Evidence Alias"], row["Evidence Alias 2"], row["Evidence Alias 3"]]
        return alias_mapping_dict


