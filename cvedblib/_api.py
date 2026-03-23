"""
API 层：注册 CVE 模块、查询、执行。
"""
from . import config
from .localization import fcall


def regist(cve_id, tags, versions, exploit_func, os_name):
    """
    注册一个 CVE 漏洞。
    :param cve_id: str, CVE 编号
    :param tags: list of str, 标签（如 'privilege_escalation', 'path_traversal'）
    :param versions: list of str, 适用的系统版本（如 ['10', '11', '12']）
    :param exploit_func: callable, 利用函数，接受 **kwargs
    :param os_name: str, 操作系统名称（如 'android', 'windows'）
    """
    config.CVE_REGISTRY[cve_id] = {
        'tags': tags,
        'versions': versions,
        'exploit': exploit_func,
        'os': os_name
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
        # 操作系统匹配
        if os is not None and info.get('os', '').lower() != os.lower():
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


def set_language(lang):
    """设置本地化语言"""
    from .localization import set_language as _set_lang
    _set_lang(lang)