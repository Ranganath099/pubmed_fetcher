import re
from typing import Any, Optional


def safe_get(obj: dict, *keys: str) -> Optional[Any]:
    for key in keys:
        if isinstance(obj, dict) and key in obj:
            obj = obj[key]
        else:
            return None
    return obj


def extract_email(text: str) -> Optional[str]:
    if not text:
        return None
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None


def debug_log(message: str, enabled: bool = False):
    if enabled:
        print(f"[DEBUG] {message}")
