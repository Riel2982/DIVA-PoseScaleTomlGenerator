# pstg_translation.py

# コンソールメッセージの多言語対応辞書（Language = ja の時は日本語で表示）
CONSOLE_MESSAGES = {
    'en': {
        'config_not_found': "The configuration file cannot be found.",
        'invalid_farcpack': "Invalid FarcPack path is set.",
        'editor_not_found': "Error: The settings editor cannot be found: {}",
        'press_enter_exit': "Press Enter to exit...",
        'usage':            "Usage: Drag and drop a file onto this executable, or use the 'Send to' menu.",
        'finished':         "Finished!",
        'unexpected_error': "An unexpected error occurred: {}",
    },
    'ja': {
        'config_not_found': "設定ファイルが見つかりません。",
        'invalid_farcpack': "FarcPackのパスが無効です。",
        'editor_not_found': "エラー: 設定エディタが見つかりません: {}",
        'press_enter_exit': "Enterキーを押して終了してください...",
        'usage':            "使い方: このアプリ（exeファイル）にファイルをドラッグ＆ドロップするか、「送る」メニューを使用してください。",
        'finished':         "Finish!",
        'unexpected_error': "予期せぬエラーが発生しました: {}",
    }
}


def get_msg(key, lang='en', *args):
    """言語設定に応じたコンソールメッセージを返す"""
    messages = CONSOLE_MESSAGES.get(lang, CONSOLE_MESSAGES['en'])
    msg = messages.get(key, CONSOLE_MESSAGES['en'].get(key, key))
    if args:
        return msg.format(*args)
    return msg