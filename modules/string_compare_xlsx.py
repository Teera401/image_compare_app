import pandas as pd


class StringCompareSlsx:
    
    @staticmethod
    def load_data_xls(file_path):
        header_dict = dict()
        para_dict = dict()
        sheet_head = 'Head-New'
        sheet_para = 'Para-New'
        df_head = pd.read_excel(file_path, sheet_name=sheet_head)
        df_para = pd.read_excel(file_path, sheet_name=sheet_para)
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
                    
        


        __read_data(df_head, header_dict)
        __read_data(df_para, para_dict)

        return header_dict, para_dict

    def __init__(self):
        pass
    #     self.image_ref_name = ""
    #     self.language_head_dict = dict()
    #     self.language_para_dict = dict()


    # def get_head_string(self, language):
    #     return self.language_head_dict.get(language, "")
    
    # def get_para_string(self, language):
    #     return self.language_para_dict.get(language, "")
    

if __name__ == "__main__":
    header_dict, para_dict = StringCompareSlsx.load_data_xls("C:\\Users\\tdc123admin\\Tools\\image_compare_app\\conf\\Text_String_compare_verECG_vs_ver17LGs.xlsx")
    for key, value in header_dict.items():
        print(f"Image Ref Name: {key}")
        for language, string_value in value.items():
            print(f"  Language: {language}, String Value: {string_value}")