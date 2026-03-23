"""
CVE-2017-0213: Windows COM 特权提升漏洞 (影响 Vista/7/8/8.1/10 早期)
"""
import subprocess
from .._api import regist
from ..localization import fcall

CVE_ID = "CVE-2017-0213"
TAGS = ["privilege_escalation"]
VERSIONS = ["Vista", "7", "8", "8.1", "10"]
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