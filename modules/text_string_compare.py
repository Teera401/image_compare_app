import pandas as pd


class TextStringCompare:
    
    @staticmethod
    def load_data_xls(file_path):
        result_dict = dict()
        df = pd.read_excel(file_path)
        header_dict = dict()
        for index, row in df.iterrows():
            if index == 0:
                for col_idx, col in enumerate(df.columns):
                    header_dict[col_idx] = col
            elif index > 0:

                text_string_compare = TextStringCompare()

                # text_string_compare.image_ref_name = image_ref_name
                for col_idx, cell_value in enumerate(row):
                    if col_idx == 0:
                        text_string_compare.image_ref_name = str(cell_value).split(".")[0] if pd.notna(cell_value) else ""
                        continue
                    language = header_dict.get(col_idx, f"Language_{col_idx}")
                    text_string_compare.language_ref_dict[language] = cell_value
                result_dict[text_string_compare.image_ref_name] = text_string_compare
        return result_dict

    def __init__(self):
        self.image_ref_name = ""
        self.language_ref_dict = dict()


    def get_string_by_language(self, language):
        return self.language_ref_dict.get(language, "")
    

if __name__ == "__main__":
    text_string_compare_data = TextStringCompare.load_data_xls("C:\\Users\\tdc123admin\\Tools\\image_compare_app\\conf\\Text_String_compare_verECG_vs_ver17LGs.xlsx")
    for key, value in text_string_compare_data.items():
        print(f"Image Ref Name: {key}")
        for language, string_value in value.language_ref_dict.items():
            print(f"  Language: {language}, String Value: {string_value}")