以下是为 `cvedblib` 包设计的完整代码框架。该包允许用户通过 `found` 函数根据标签、操作系统、版本等条件查询 CVE ID，并提供 `exploit` 函数执行指定漏洞的利用代码。所有用户可见的文本均支持中英文本地化，并通过 `fcall` 从 `o.json` 获取。

## 文件结构

```
cvedblib/
├── __init__.py
├── _api.py
├── config.py
├── localization.py
├── o.json
├── android/
│   ├── __init__.py
│   ├── cve_2023_12345.py
│   └── cve_2023_67890.py
├── windows/
│   ├── __init__.py
│   └── cve_2022_1234.py
├── mac/
│   └── __init__.py
└── unix/
    └── __init__.py
```

---

## 1. `cvedblib/__init__.py`

```python
"""
顶层 __init__.py 负责导入所有子包并暴露公共 API。
"""
from ._api import found, exploit, get_cve_info
from .android import *
from .windows import *
from .mac import *
from .unix import *
```

---

## 2. `cvedblib/_api.py`

提供注册函数 `regist` 和公共 API `found`、`exploit`、`get_cve_info`。

```python
"""
API 层：注册 CVE 模块、查询、执行。
"""
from . import config
from .localization import fcall


def regist(cve_id, tags, versions, exploit_func):
    """
    注册一个 CVE 漏洞。
    :param cve_id: str, CVE 编号
    :param tags: list of str, 标签（如 'privilege_escalation', 'path_traversal'）
    :param versions: list of str, 适用的系统版本（如 ['10', '11', '12']）
    :param exploit_func: callable, 利用函数，接受 **kwargs
    """
    config.CVE_REGISTRY[cve_id] = {
        'tags': tags,
        'versions': versions,
        'exploit': exploit_func
    }


def found(tags=None, os=None, version=None):
    """
    根据条件查找匹配的 CVE ID。
    :param tags: str or list, 标签（单个或列表）
    :param os: str, 操作系统（android/windows/mac/unix）
    :param version: str, 系统版本
    :return: list of str, 匹配的 CVE ID 列表
    """
    result = []
    for cve_id, info in config.CVE_REGISTRY.items():
        # 标签匹配
        if tags is not None:
            if isinstance(tags, str):
                tags = [tags]
            if not any(tag in info['tags'] for tag in tags):
                continue
        # 操作系统匹配（简单根据模块路径推断，实际可扩展）
        if os is not None:
            # 假设 CVE 模块按系统存放，可通过 info 中的 os 字段判断
            if info.get('os', '').lower() != os.lower():
                continue
        # 版本匹配
        if version is not None and version not in info['versions']:
            continue
        result.append(cve_id)
    return result


def exploit(cve_id, **kwargs):
    """
    执行指定 CVE 的利用代码。
    :param cve_id: str, CVE 编号
    :param kwargs: 传递给利用函数的参数（如 cmd）
    """
    info = config.CVE_REGISTRY.get(cve_id)
    if not info:
        print(fcall("cve_not_found").format(cve_id))
        return
    try:
        info['exploit'](**kwargs)
    except Exception as e:
        print(fcall("exploit_error").format(cve_id, str(e)))


def get_cve_info(cve_id):
    """返回 CVE 的注册信息"""
    return config.CVE_REGISTRY.get(cve_id)
```

---

## 3. `cvedblib/config.py`

全局配置和注册表。

```python
"""
全局配置：CVE 注册表。
"""
CVE_REGISTRY = {}  # 格式: {cve_id: {'tags': [...], 'versions': [...], 'exploit': func, 'os': str}}
```

---

## 4. `cvedblib/localization.py`

本地化支持，从 `o.json` 加载字符串，根据系统语言返回对应文本。

```python
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
```

---

## 5. `cvedblib/o.json`

本地化字符串库。

```json
{
    "cve_not_found": {
        "en": "CVE {0} not found.",
        "zh": "未找到 CVE {0}。"
    },
    "exploit_error": {
        "en": "Error executing {0}: {1}",
        "zh": "执行 {0} 时出错：{1}"
    },
    "exploit_start": {
        "en": "Executing {0}...",
        "zh": "正在执行 {0}..."
    },
    "exploit_success": {
        "en": "Exploit executed successfully.",
        "zh": "漏洞利用成功。"
    },
    "command_output": {
        "en": "Command output:\n{0}",
        "zh": "命令输出：\n{0}"
    }
}
```

---

## 6. `cvedblib/android/__init__.py`

按需求：`__all__` 列出所有模块名，`from . import *` 导入所有模块。

```python
__all__ = ["cve_2023_12345", "cve_2023_67890"]
from . import *
```

---

## 7. `cvedblib/android/cve_2023_12345.py`

示例：提权漏洞，支持 `cmd` 参数。

```python
"""
CVE-2023-12345: Android 提权漏洞
"""
import subprocess
from .._api import regist
from ..localization import fcall

CVE_ID = "CVE-2023-12345"
TAGS = ["privilege_escalation"]
VERSIONS = ["10", "11", "12", "13"]


def exploit(cmd="whoami"):
    """
    执行提权并运行命令。
    """
    print(fcall("exploit_start").format(CVE_ID))
    # 模拟提权后执行命令
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
        print(fcall("command_output").format(output))
        print(fcall("exploit_success"))
    except Exception as e:
        print(fcall("exploit_error").format(CVE_ID, str(e)))


# 注册
regist(CVE_ID, TAGS, VERSIONS, exploit)
# 可选：记录操作系统，便于查询时按系统过滤
from ..config import CVE_REGISTRY
CVE_REGISTRY[CVE_ID]['os'] = 'android'
```

---

## 8. `cvedblib/android/cve_2023_67890.py`

示例：路径遍历漏洞，无额外参数。

```python
"""
CVE-2023-67890: Android 路径遍历漏洞
"""
from .._api import regist
from ..localization import fcall

CVE_ID = "CVE-2023-67890"
TAGS = ["path_traversal"]
VERSIONS = ["11", "12"]


def exploit(**kwargs):
    """
    路径遍历利用（演示）。
    """
    print(fcall("exploit_start").format(CVE_ID))
    # 实际利用代码...
    print(fcall("exploit_success"))


regist(CVE_ID, TAGS, VERSIONS, exploit)
from ..config import CVE_REGISTRY
CVE_REGISTRY[CVE_ID]['os'] = 'android'
```

---

## 9. `cvedblib/windows/__init__.py`

```python
__all__ = ["cve_2022_1234"]
from . import *
```

---

## 10. `cvedblib/windows/cve_2022_1234.py`

示例：Windows 漏洞。

```python
"""
CVE-2022-1234: Windows 本地提权
"""
from .._api import regist
from ..localization import fcall
import subprocess

CVE_ID = "CVE-2022-1234"
TAGS = ["privilege_escalation"]
VERSIONS = ["10", "11"]


def exploit(cmd="whoami"):
    print(fcall("exploit_start").format(CVE_ID))
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(fcall("command_output").format(result.stdout or result.stderr))
    print(fcall("exploit_success"))


regist(CVE_ID, TAGS, VERSIONS, exploit)
from ..config import CVE_REGISTRY
CVE_REGISTRY[CVE_ID]['os'] = 'windows'
```

---

## 11. 其他子包 `mac/__init__.py`、`unix/__init__.py`

这两个子包可以保持为空（只包含 `__init__.py`），或者添加示例 CVE 文件，结构与上述类似。

`mac/__init__.py`:
```python
__all__ = []  # 暂无 CVE
from . import *
```

`unix/__init__.py`:
```python
__all__ = []
from . import *
```

---

## 使用示例

```python
import cvedblib

# 查询所有提权漏洞
escalation_cves = cvedblib.found(tags="privilege_escalation")
print(escalation_cves)  # ['CVE-2023-12345', 'CVE-2022-1234']

# 查询 Android 上的漏洞
android_cves = cvedblib.found(os="android")
print(android_cves)  # ['CVE-2023-12345', 'CVE-2023-67890']

# 查询指定版本
specific = cvedblib.found(os="android", version="13")
print(specific)  # ['CVE-2023-12345']

# 执行漏洞
cvedblib.exploit("CVE-2023-12345", cmd="id")
```

输出会随语言环境自动切换（中文或英文）。

---

## 扩展说明

- **添加新 CVE**：在对应系统子包中创建 `cve_xxxx_xxx.py`，定义 `exploit` 函数，调用 `regist` 注册，并添加 `os` 信息到注册表即可。
- **支持更多标签**：只需在注册时传入新标签，`found` 函数会匹配。
- **版本匹配**：可进一步实现版本范围解析（如 `>=10`），当前示例为精确匹配，可自行扩展。
- **本地化**：预留了 `set_language` 函数，用户可手动切换语言；新增语言只需在 `o.json` 中添加对应键值。