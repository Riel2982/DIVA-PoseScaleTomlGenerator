# pstg_scale.py

import logging
from pstg_util import is_match

def generate_scale_toml(module_data, scale_settings, map_chara):
    """Scale TOMLデータを生成する"""
    scale_toml_entries = []
    logging.info("ScaleTomlデータの変換を開始")

    # モジュールデータを走査
    for module_value in module_data:
        module_chara = map_chara(module_value["chara"], "module_to_setting") # モジュールキャラクター
        
        # First pass: Specific matches (ModuleNameContains is set)（特定の一致）
        matched = False
        # Pose設定を走査
        for setting in scale_settings:
            match_str = setting["ModuleNameContains"] # マッチング文字列
            if match_str: # Specific（特定の一致）
                if module_chara == setting["Chara"]: # キャラクターが一致
                    if is_match(module_value["name"], match_str, setting.get("ModuleExclude")): # マッチング
                        # Apply setting（設定を適用する）
                        if setting["Scale"] is not None and str(setting["Scale"]).strip(): # Scaleが設定されているかつ空でない
                            chara_value = map_chara(module_value["chara"], "module_to_cos_scale") # キャラクター値
                            cos_value = int(module_value["cos"].replace("COS_", "")) - 1 # COS値
                            scale_value = setting["Scale"] # Scale値

                            # TOMLエントリを生成
                            entry = f'[[cos_scale]]\nchara = {chara_value}\ncos = {cos_value}\nscale = {scale_value}\n'
                            scale_toml_entries.append(entry) # Scale TOMLデータ
                            logging.debug(f"Scaleを設定 (Specific): Module={module_value['name']}, Scale={scale_value}")
                        matched = True
                        break
        
        # Second pass: Fallback matches (ModuleNameContains is empty)（一致しない場合）
        if not matched:
            for setting in scale_settings: # Scale設定を走査
                match_str = setting["ModuleNameContains"] # マッチング文字列
                if not match_str: # Fallback
                    if module_chara == setting["Chara"]: # キャラクターが一致
                        # Check excludes manually since is_match returns False for empty match_str（一致しない場合）
                        exclude_str = setting.get("ModuleExclude") # 除外文字列
                        is_excluded = False # 除外フラグ
                        if exclude_str: # 除外文字列が設定されている
                             excludes = [word.strip() for word in exclude_str.split(',') if word.strip()] # 除外文字列をリストに変換
                             if any(exc in module_value["name"] for exc in excludes): # 除外文字列が一致
                                 is_excluded = True # 除外フラグ
                        
                        if not is_excluded: # 除外文字列が一致しない場合
                            # Apply setting（設定を適用する）
                            if setting["Scale"] is not None and str(setting["Scale"]).strip(): # Scaleが設定されているかつ空でない
                                chara_value = map_chara(module_value["chara"], "module_to_cos_scale") # キャラクター値
                                cos_value = int(module_value["cos"].replace("COS_", "")) - 1 # COS値
                                scale_value = setting["Scale"] # Scale値

                                entry = f'[[cos_scale]]\nchara = {chara_value}\ncos = {cos_value}\nscale = {scale_value}\n'
                                scale_toml_entries.append(entry)
                                logging.debug(f"Scaleを設定 (Fallback): Module={module_value['name']}, Scale={scale_value}")
                            matched = True
                            break
                            
        if not matched:
             logging.debug(f"マッチする設定が見つかりませんでした: {module_value['name']}")

    return scale_toml_entries
