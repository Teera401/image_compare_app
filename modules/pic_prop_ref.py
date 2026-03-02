import os
import re

class PicPropRef:
    def __init__(self, language=None, alias=None, full_path=None):
        # self.ref_id = ref_id
        self.language = language
        aliastmp = re.sub(r'[^a-zA-Z0-9_,]', '', (alias.split(".")[0])) if alias else None
        self.alias = aliastmp.lower() if aliastmp else None
        self.full_path = full_path
        self.pic_name_without_exten = (os.path.basename(full_path).split(".")[0]) if full_path else None
        self.hash_value = "" #self.__calculate_hash() if full_path else None
   
    def __calculate_hash(self):
        import hashlib
        hash_md5 = hashlib.md5()
        with open(self.full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

        