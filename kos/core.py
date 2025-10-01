"""
核心模块 (Core module)
"""

import logging
import subprocess
import sys
from typing import List, Optional, Dict, Any
from .config import Config


class KOS:
    """KOS核心类，负责代码自动发射/部署"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        初始化KOS
        
        Args:
            config: 配置对象，如果为None则使用默认配置
        """
        self.config = config or Config()
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
    
    def _setup_logging(self):
        """设置日志"""
        level = getattr(logging, self.config.get('logging.level', 'INFO'))
        log_file = self.config.get('logging.file')
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                *([logging.FileHandler(log_file)] if log_file else [])
            ]
        )
    
    def execute_command(self, command: str, shell: bool = True) -> Dict[str, Any]:
        """
        执行命令
        
        Args:
            command: 要执行的命令
            shell: 是否在shell中执行
            
        Returns:
            包含返回码、输出和错误信息的字典
        """
        self.logger.info(f"执行命令: {command}")
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=300
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            self.logger.error(f"命令执行超时: {command}")
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "命令执行超时",
                "success": False
            }
        except Exception as e:
            self.logger.error(f"命令执行失败: {e}")
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False
            }
    
    def deploy(self, target: Optional[str] = None, commands: Optional[List[str]] = None) -> bool:
        """
        执行部署
        
        Args:
            target: 部署目标
            commands: 要执行的命令列表
            
        Returns:
            部署是否成功
        """
        target = target or self.config.get('deployment.target', 'local')
        self.logger.info(f"开始部署到目标: {target}")
        
        if commands is None:
            commands = self._get_default_commands(target)
        
        success = True
        for cmd in commands:
            result = self.execute_command(cmd)
            if not result['success']:
                self.logger.error(f"命令执行失败: {cmd}")
                self.logger.error(f"错误信息: {result['stderr']}")
                success = False
                break
            else:
                self.logger.info(f"命令执行成功: {cmd}")
                if result['stdout']:
                    self.logger.info(f"输出: {result['stdout']}")
        
        if success:
            self.logger.info(f"部署成功完成")
        else:
            self.logger.error(f"部署失败")
        
        return success
    
    def _get_default_commands(self, target: str) -> List[str]:
        """
        获取默认部署命令
        
        Args:
            target: 部署目标
            
        Returns:
            命令列表
        """
        if target == 'local':
            return [
                'echo "本地部署开始"',
                'echo "检查环境..."',
                'echo "部署完成"'
            ]
        else:
            return [f'echo "部署到 {target}"']
    
    def launch(self, script: Optional[str] = None) -> bool:
        """
        启动/发射代码
        
        Args:
            script: 要执行的脚本路径
            
        Returns:
            是否成功
        """
        self.logger.info(f"启动代码发射流程")
        
        if script:
            result = self.execute_command(f"python {script}")
            return result['success']
        else:
            self.logger.info("没有指定脚本，使用默认发射流程")
            return self.deploy()
    
    def status(self) -> Dict[str, Any]:
        """
        获取当前状态
        
        Returns:
            状态信息字典
        """
        return {
            "version": self.config.get('version', '0.1.0'),
            "deployment_type": self.config.get('deployment.type', 'default'),
            "target": self.config.get('deployment.target', 'local'),
            "auto_start": self.config.get('deployment.auto_start', False)
        }
