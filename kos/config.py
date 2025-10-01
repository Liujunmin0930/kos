"""
配置管理模块 (Configuration management module)
"""

import os
import yaml
from typing import Dict, Any, Optional


class Config:
    """配置类，用于管理KOS配置"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """返回默认配置"""
        return {
            "name": "kos",
            "version": "0.1.0",
            "deployment": {
                "type": "default",
                "target": "local",
                "auto_start": False
            },
            "logging": {
                "level": "INFO",
                "file": None
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套键，如 "deployment.type"
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """
        设置配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None):
        """
        保存配置到文件
        
        Args:
            path: 保存路径，如果为None则使用初始化时的路径
        """
        save_path = path or self.config_path
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
