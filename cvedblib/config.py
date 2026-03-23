"""
全局配置：CVE 注册表。
"""
CVE_REGISTRY = {}  # 格式: {cve_id: {'tags': [...], 'versions': [...], 'exploit': func, 'os': str}}