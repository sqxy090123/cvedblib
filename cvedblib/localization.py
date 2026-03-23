import json
import locale
import os
from pathlib import Path

# 加载 o.json
_O_JSON_PATH = Path(__file__).parent / "o.json"
with open(_O_JSON_PATH, 'r', encoding='utf-8') as f:
    _STRINGS = json.load(f)

# 检测语言（优先使用环境变量 LANG，否则取系统 locale）
_current_lang = 'en'
try:
    lang = os.environ.get('LANG', locale.getlocale()[0] or 'en')
    if lang.startswith('zh'):
        _current_lang = 'zh'
    else:
        _current_lang = 'en'
except:
    _current_lang = 'en'


def set_language(lang):
    """手动设置语言，支持 'en' 或 'zh'"""
    global _current_lang
    if lang in ('en', 'zh'):
        _current_lang = lang


def fcall(key, **kwargs):
    """
    获取本地化字符串。
    :param key: 字符串键名
    :param kwargs: 格式化参数
    """
    item = _STRINGS.get(key, {})
    text = item.get(_current_lang, item.get('en', key))
    if kwargs:
        text = text.format(**kwargs)
    return text