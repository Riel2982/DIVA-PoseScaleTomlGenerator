# pstg_pose.py

import logging
from pstg_util import is_match

def generate_pose_toml(module_data, pose_settings, map_chara):
    """Pose TOMLデータを生成する"""
    pose_toml_entries = [] # Pose TOMLデータ
    logging.info("PoseTomlデータの変換を開始")

    # モジュールデータを走査
    for module_value in module_data:
        module_chara = map_chara(module_value["chara"], "module_to_setting") # モジュールキャラクター
        
        # First pass: Specific matches (ModuleNameContains is set)（特定のマッチング）
        matched = False # マッチングフラグ
        # Pose設定を走査
        for setting in pose_settings:
            match_str = setting["ModuleNameContains"] # マッチング文字列
            if match_str: # Specific（特定のマッチング）
                if module_chara == setting["Chara"]: # キャラクターが一致
                    if is_match(module_value["name"], match_str, setting.get("ModuleExclude")): # マッチング
                        if setting["PoseID"] is not None and str(setting["PoseID"]).strip(): # PoseIDが設定されているかつ空でない
                            pose_toml_entries.append(f'{module_value["id"]} = {setting["PoseID"]}') # Pose TOMLデータ
                            logging.debug(f"PoseIDを設定 (Specific): Module={module_value['name']}, ID={module_value['id']}, PoseID={setting['PoseID']}")
                        matched = True # マッチングフラグ
                        break

        # Second pass: Fallback matches (ModuleNameContains is empty)（特定のマッチングがない場合）
        if not matched:
            for setting in pose_settings:
                match_str = setting["ModuleNameContains"] # マッチング文字列
                if not match_str: # Fallback（特定のマッチングがない場合）
                    if module_chara == setting["Chara"]: # キャラクターが一致
                        # Check excludes manually（除外文字列を手動でチェック）
                        exclude_str = setting.get("ModuleExclude") # 除外文字列
                        is_excluded = False # 除外フラグ
                        if exclude_str: # 除外文字列が設定されている
                             excludes = [word.strip() for word in exclude_str.split(',') if word.strip()] # 除外文字列をリストに変換
                             if any(exc in module_value["name"] for exc in excludes): # 除外文字列が一致
                                 is_excluded = True # 除外フラグ
                        
                        # 除外文字列が一致しない場合
                        if not is_excluded:
                            # PoseIDが設定されている場合
                            if setting["PoseID"] is not None and str(setting["PoseID"]).strip():
                                pose_toml_entries.append(f'{module_value["id"]} = {setting["PoseID"]}') # Pose TOMLデータ
                                logging.debug(f"PoseIDを設定 (Fallback): Module={module_value['name']}, ID={module_value['id']}, PoseID={setting['PoseID']}")
                            matched = True # マッチングフラグ
                            break
                            
        if not matched:
             logging.debug(f"マッチするPose設定が見つかりませんでした: {module_value['name']}")

    return pose_toml_entries

