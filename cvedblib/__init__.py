"""
顶层 __init__.py 负责导入所有子包并暴露公共 API。
"""
from ._api import found, exploit, get_cve_info, set_language
from .android import *
from .windows import *
from .mac import *
from .unix import *