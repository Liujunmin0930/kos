"""
KOS - 自动发射代码工具 (Automatic Deployment Code Tool)
"""

__version__ = "0.1.0"

from .core import KOS
from .config import Config

__all__ = ["KOS", "Config"]
