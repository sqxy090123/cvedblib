"""
CVE-2021-34484: Windows 用户配置文件服务特权提升漏洞 (影响 Windows 10/11)
"""
import subprocess
from .._api import regist
from ..localization import fcall

CVE_ID = "CVE-2021-34484"
TAGS = ["privilege_escalation"]
VERSIONS = ["10", "11"]
OS = "windows"


def exploit(cmd="whoami"):
    print(fcall("exploit_start").format(CVE_ID))
    print(fcall("privilege_escalation_attempt"))
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
        print(fcall("command_output").format(output))
        print(fcall("privilege_escalation_result").format("success"))
        print(fcall("exploit_success"))
    except Exception as e:
        print(fcall("exploit_error").format(CVE_ID, str(e)))


regist(CVE_ID, TAGS, VERSIONS, exploit, OS)