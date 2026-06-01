# pstg_extract.py

import os
import json
import logging
from pstg_util import get_temp_dir

def load_and_combine_text_data():
    """Tempディレクトリ内のBINファイルを読み込んで結合する"""
    temp_dir = get_temp_dir()
    text_data = ''
    
    # gm_module_tblフォルダを検索する。
    gm_module_tbl_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d)) and 'gm_module_tbl' in d]
    
    # gm_module_tblフォルダが見つからない場合、ログを出力する。
    if not gm_module_tbl_dirs:
        logging.error("Tempディレクトリにgm_module_tblフォルダが存在しません")
        return ""
    
    # gm_module_tblフォルダ内のファイルを検索する。
    for dir_name in gm_module_tbl_dirs:
        gm_module_tbl_path = os.path.join(temp_dir, dir_name)
        # gm_module_tblフォルダ内のファイルを検索する。
        for file_name in os.listdir(gm_module_tbl_path):
            # BINファイルを検索する。
            if file_name.endswith('.bin'):
                try:
                    # BINファイルを読み込む。
                    with open(os.path.join(gm_module_tbl_path, file_name), 'r', encoding='utf-8') as file:
                        content = file.read()
                        # BINファイルの内容を結合する。
                        if content:
                            text_data += content
                            logging.debug(f"{file_name} の内容: {content}")
                            logging.info(f"Binファイルを正常に読み込みました: {file_name}")
                        else:
                            # 空のファイルをスキップする。
                            logging.warning(f"空のファイルをスキップしました: {file_name}")
                except Exception as e:
                    # ファイルの読み込みに失敗した場合、ログを出力する。
                    logging.error(f"ファイルの読み込みに失敗しました {file_name}: {e}")

    # BINファイルの内容を結合する。
    if not text_data:
        logging.error("BINファイルからデータを読み込めませんでした")
        return ""

    # BINデータを結合する。
    combined_data = f'BINデータ\n{text_data}\n'
    logging.info(f"combined_data を正常に読み込みました")
    return combined_data

def process_data():
    """BINデータを解析してJSONとして保存し、辞書データを返す"""
    try:
        # BINデータを結合する。
        combined_data = load_and_combine_text_data()
        # BINデータを結合できなかった場合、ログを出力する。
        if not combined_data:
            logging.error("BINデータを結合できませんでした")
            return []

        modules_by_id = {} # モジュールIDをキーとする辞書
        
        # BINデータを解析する。
        for line in combined_data.splitlines():
            line = line.strip()
            # module.で始まる行を解析する。
            if not line.startswith('module.'):
                continue
            
            # =で区切る。
            if '=' in line:
                key_part, value = line.split('=', 1) # キーと値で区切る。
                key_part = key_part.strip() # キー部分を空白文字を削除する。
                value = value.strip() # 値部分を空白文字を削除する。
                
                # module_numとkeyで区切る。
                parts = key_part.split('.')
                if len(parts) < 3:
                    continue
                
                module_num = parts[1] # モジュール番号
                key = parts[2] # キー
                
                # chara, cos, id, nameで区切る。
                if key in ['chara', 'cos', 'id', 'name']:
                    # モジュール番号をキーとする辞書に値を格納する。
                    if module_num not in modules_by_id:
                        modules_by_id[module_num] = {"module_num": module_num} # モジュール番号をキーとする辞書
                    
                    modules_by_id[module_num][key] = value # モジュール番号をキーとする辞書に値を格納する。

        module_data_list = list(modules_by_id.values()) # モジュール番号をキーとする辞書をリストに変換する。
        module_data_dict = {"modules": module_data_list} # モジュール番号をキーとする辞書を辞書に変換する。

        temp_dir = get_temp_dir() # 一時ディレクトリ
        module_data_path = os.path.join(temp_dir, 'module_data.json') # モジュールデータのパス
        
        # モジュールデータを保存する。
        with open(module_data_path, 'w', encoding='utf-8') as json_file:
            json.dump(module_data_dict, json_file, ensure_ascii=False, indent=4)

        logging.info(f"module_data.json を保存しました: {module_data_path}")
        return module_data_list

    except Exception as e:
        logging.error(f"Error in process_data: {e}")
        raise
