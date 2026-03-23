"""
CVE-2023-67890: Android 路径遍历漏洞
"""
from .._api import regist
from ..localization import fcall

CVE_ID = "CVE-2023-67890"
TAGS = ["path_traversal"]
VERSIONS = ["11", "12"]
OS = "android"


def exploit(**kwargs):
    """
    路径遍历利用（演示）。
    """
    print(fcall("exploit_start").format(CVE_ID))
    # 实际利用代码...
    print(fcall("exploit_success"))


regist(CVE_ID, TAGS, VERSIONS, exploit, OS)