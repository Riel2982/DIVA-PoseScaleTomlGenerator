# pstg_config.py

import configparser
import os
import logging
from pstg_util import get_app_dir

def load_app_config():
    """アプリケーション設定を読み込む"""
    app_dir = get_app_dir()
    settings_dir = os.path.join(app_dir, 'Settings')
    
    # Ensure Settings directory exists (migration or fresh start)（設定ディレクトリが存在するか、または新しい設定ディレクトリを作成するか）
    if not os.path.exists(settings_dir):
        # 設定ディレクトリが見つからない場合、Settingsをチェックし、次にrootをチェックする。
        pass

    ini_path = os.path.join(settings_dir, 'Config.ini') # 設定ファイルのパス
    if not os.path.exists(ini_path):
        ini_path = os.path.join(app_dir, 'Config.ini') # 設定ファイルが見つからない場合、アプリケーションのディレクトリをチェックする。

    profile_path = os.path.join(settings_dir, 'TomlProfile.ini') # プロファイル設定ファイルのパス
    
    config = configparser.ConfigParser() # ConfigParserオブジェクトを作成する。
    try:
        config.read(ini_path, encoding='utf-8-sig') # 設定ファイルを読み込む。
    except Exception as e:
        logging.error(f"設定ファイルの読み込みに失敗しました: {e}")

    profile_config = configparser.ConfigParser() # ConfigParserオブジェクトを作成する。
    if os.path.exists(profile_path):
        try:
            profile_config.read(profile_path, encoding='utf-8-sig')
        except Exception as e:
            logging.error(f"プロファイル設定の読み込みに失敗しました: {e}")
    else:
        # Fallback: use main config as profile config if profiles are there（プロファイルが存在する場合、メイン設定をプロファイル設定として使用する）
        profile_config = config

    # app_config（アプリケーション設定）
    app_config = {
        # FarcPackPath（ファルクパックのパス）
        'FarcPackPath': config.get('FarcPack', 'FarcPackPath', fallback='').strip('"'),
        # DefaultPoseFileName（デフォルトのポーズファイル名）
        'DefaultPoseFileName': config.get('GeneralSettings', 'DefaultPoseFileName', fallback='pose_data'),
        # SaveInParentDirectory（親ディレクトリに保存する）
        'SaveInParentDirectory': config.getboolean('GeneralSettings', 'SaveInParentDirectory', fallback=False),
        # OverwriteExistingFiles（既存のファイルを上書きする）
        'OverwriteExistingFiles': config.getboolean('GeneralSettings', 'OverwriteExistingFiles', fallback=False),
        # UseModuleNameContains（モジュール名を含める）
        'UseModuleNameContains': config.getboolean('GeneralSettings', 'UseModuleNameContains', fallback=False),
        
        # UpdateConfigToml（config.toml の module_poses セクションに設定を挿入する）
        'UpdateConfigToml': config.getboolean('GeneralSettings', 'UpdateConfigToml', fallback=False),
        
        # Language（言語）
        'Language': config.get('GeneralSettings', 'Language', fallback='en'),
        # ShowDebugSettings（デバッグ設定を表示する）
        # 'ShowDebugSettings': config.getboolean('DebugSettings', 'ShowDebugSettings', fallback=False),
        # OutputLog（出力ログ）
        'OutputLog': config.getboolean('DebugSettings', 'OutputLog', fallback=False),
        # DeleteTemp（一時ファイルを削除する）
        'DeleteTemp': config.getboolean('DebugSettings', 'DeleteTemp', fallback=True),
        # HistoryLimit（履歴制限）
        # 'HistoryLimit': config.getint('DebugSettings', 'HistoryLimit', fallback=50),
        'ConfigParser': config, # Main config（メイン設定）
        'ProfileConfig': profile_config, # Profile config（プロファイル設定）
        'SettingsDir': settings_dir # Expose settings dir for other modules（他のモジュール用の設定ディレクトリ）
    }
    
    logging.info(f"設定を読み込みました: {app_config}")
    return app_config
