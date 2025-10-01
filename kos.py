#!/usr/bin/env python3
"""
kos - 自动发射代码 (Automatic Code Launcher)
A simple tool for automatically launching and executing code/scripts
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path


class KOS:
    """KOS - Automatic Code Launcher"""
    
    def __init__(self, config_path='config.json'):
        """Initialize KOS with configuration"""
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def launch(self, target=None):
        """Launch the specified target or default target"""
        if target is None:
            target = self.config.get('default_target', None)
            if target is None:
                print("错误: 未指定目标且配置中没有默认目标 (No target specified and no default in config)")
                return False
        
        targets = self.config.get('targets', {})
        if target not in targets:
            print(f"错误: 目标 '{target}' 未在配置中找到 (Target not found in config)")
            return False
        
        target_config = targets[target]
        return self.execute(target_config)
    
    def execute(self, target_config):
        """Execute a target configuration"""
        command = target_config.get('command')
        if not command:
            print("错误: 目标配置中没有命令 (No command in target config)")
            return False
        
        working_dir = target_config.get('working_dir', '.')
        env = os.environ.copy()
        env.update(target_config.get('env', {}))
        
        print(f"发射代码... (Launching code...)")
        print(f"命令 (Command): {command}")
        print(f"工作目录 (Working directory): {working_dir}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_dir,
                env=env,
                capture_output=False
            )
            
            if result.returncode == 0:
                print(f"\n✓ 成功! (Success!)")
                return True
            else:
                print(f"\n✗ 失败，退出码: {result.returncode} (Failed with exit code: {result.returncode})")
                return False
                
        except Exception as e:
            print(f"\n✗ 执行错误 (Execution error): {e}")
            return False
    
    def list_targets(self):
        """List all available targets"""
        targets = self.config.get('targets', {})
        if not targets:
            print("没有配置的目标 (No configured targets)")
            return
        
        print("可用目标 (Available targets):")
        default = self.config.get('default_target')
        for name, target in targets.items():
            is_default = " [默认/default]" if name == default else ""
            print(f"  - {name}{is_default}")
            print(f"    命令 (Command): {target.get('command', 'N/A')}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='kos - 自动发射代码 (Automatic Code Launcher)'
    )
    parser.add_argument(
        'target',
        nargs='?',
        help='要发射的目标 (Target to launch)'
    )
    parser.add_argument(
        '-c', '--config',
        default='config.json',
        help='配置文件路径 (Config file path, default: config.json)'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='列出所有可用目标 (List all available targets)'
    )
    
    args = parser.parse_args()
    
    kos = KOS(config_path=args.config)
    
    if args.list:
        kos.list_targets()
    elif args.target or kos.config.get('default_target'):
        success = kos.launch(args.target)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
