
import os
from pathlib import Path
import re

from modules.pic_prop_ref import PicPropRef


class PicPropEvidence:
    def __init__(self, full_path=None):

        alias = re.sub(r'[^a-zA-Z0-9_,]', '', (os.path.basename(full_path).split(".")[0])) if full_path else None
        alias_match = re.search(r'Step\d+(.*)_screen', alias, re.IGNORECASE)
        alias_match = re.search(r'Step\d+(.*)', alias, re.IGNORECASE) if not alias_match else alias_match
        pic_step_match = re.search(r'Step(\d+)', alias, re.IGNORECASE)
        self.alias = alias_match.group(1).lower() if alias_match else alias
        self.step = pic_step_match.group(1) if pic_step_match else ""
        self.pic_name = os.path.basename(full_path) if full_path else None
        self.key = None
        self.vpt_name = None
        self.test_case_name = None
        self.full_path = full_path
        self.PicPropRef = None
        for dir in Path(full_path).parent.parents:
            if re.match(r'^VTP\d+$', dir.name, re.IGNORECASE):
                self.vpt_name = dir.name    
                break 
        for dir in Path(full_path).parent.parents:
            matchVtpKey =  re.match(r'^(VTP\d+_.*)', dir.name, re.IGNORECASE)
            matchTc =  re.match(r'^(VTP\d+_\d+)', dir.name, re.IGNORECASE)
            if matchTc:                
                self.test_case_name = matchTc.group(1)
            if matchVtpKey:
                self.key = f"{matchVtpKey.group(1)}_{self.pic_name}"
                break       
    def set_picprop_ref(self, alias_mapping_config_dict, refer_data_mapping_list, language_mapping):
        if not self.alias or not alias_mapping_config_dict or not refer_data_mapping_list:
            return
        
        language = language_mapping.get(self.test_case_name, None)
        ref_alias_select = None
        for ref_alias, evidence_aliases in alias_mapping_config_dict.items():
            if self.alias in evidence_aliases:
                # self.key = f"{ref_alias}_{self.alias}"
                ref_alias_select = ref_alias
                break
        if ref_alias_select and language:
            for pic_prop_ref in refer_data_mapping_list:
                pic_prop_ref: PicPropRef
                if pic_prop_ref.alias == ref_alias_select and pic_prop_ref.language == language:
                    # self.key = f"{pic_prop_ref.alias}_{self.alias}"
                    self.PicPropRef = pic_prop_ref
                    break