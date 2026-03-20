
import os
from pathlib import Path
import re

from modules.evidence_alias import EvidenceAlias
from modules.pic_prop_ref import PicPropRef


class PicPropEvidence:
    def __init__(self, full_path=None):

        alias = re.sub(r'[^a-zA-Z0-9_,]', '', (os.path.basename(full_path).split(".")[0])) if full_path else None
        alias_match = re.search(r'Step\d+(.*)_screen', alias, re.IGNORECASE)
        alias_match = re.search(r'Step\d+(.*)', alias, re.IGNORECASE) if not alias_match else alias_match
        pic_step_match = re.search(r'Step(\d+)', alias, re.IGNORECASE)
        self.aliasFileName = alias_match.group(1).lower() if alias_match else alias
        self.step = pic_step_match.group(1) if pic_step_match else ""
        self.pic_name = os.path.basename(full_path) if full_path else None
        self.key = None
        self.vpt_name = None
        self.test_case_name = None
        self.full_path = full_path
        self.picPropRefList = list()
        self.languageRef = None
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
        if not self.aliasFileName or not alias_mapping_config_dict or not refer_data_mapping_list:
            return
        
        language = language_mapping.get(self.test_case_name, None)
        ref_alias_select = list() #list of EvidenceAlias
        for ref_alias, evidence_aliases in alias_mapping_config_dict.items():
            evidence_aliases:EvidenceAlias
            if evidence_aliases.iscompitible_refalias(self.aliasFileName):
                if not evidence_aliases.haveGroup():
                    ref_alias_select.append(evidence_aliases)
                    break
                else:
                   ref_alias_select = evidence_aliases.alias_membergroup_ls
        if len(ref_alias_select) > 0 and language != None:
            self.languageRef = language
            for refaselect in ref_alias_select:
                refaselect:EvidenceAlias
                filtered_people = list(filter(lambda pic_prop_ref: pic_prop_ref.alias == refaselect.ref_alias and pic_prop_ref.language == language, refer_data_mapping_list))
                self.picPropRefList = self.picPropRefList + filtered_people
                

            # for pic_prop_ref in refer_data_mapping_list:
            #     pic_prop_ref: PicPropRef
            #     if ref_alias_select.ref_alias == pic_prop_ref.alias and pic_prop_ref.language == language:
            #         # if ref_alias_select.haveGroup():
            #         self.picPropRef = pic_prop_ref
            #         self.languageRef = language
            #         break

    # def getPicPropRefMember(self, listEvidenceAlias):
    #     resultPicPropRefLs = list()
    #     # for evdAlias in listEvidenceAlias:

    #     return resultPicPropRefLs