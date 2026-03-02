
from modules.setting_cnf_provider import SettingCnfProvider


if __name__ == "__main__":

    settingCnf = SettingCnfProvider()
    # settingCnf.write_language_mapping_config()
    # settingCnf.write_refer_data_mapping_config()
    # settingCnf.write_evidence_mapping_config()
    settingCnf.write_alias_mapping_config()

    pass