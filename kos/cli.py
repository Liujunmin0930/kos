"""
命令行接口模块 (CLI module)
"""

import click
import sys
from pathlib import Path
from .core import KOS
from .config import Config


@click.group()
@click.version_option(version='0.1.0')
@click.option('--config', '-c', type=click.Path(exists=True), help='配置文件路径')
@click.pass_context
def main(ctx, config):
    """
    KOS - 自动发射代码工具
    
    一个用于自动部署和发射代码的命令行工具。
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config) if config else Config()
    ctx.obj['kos'] = KOS(ctx.obj['config'])


@main.command()
@click.option('--target', '-t', default=None, help='部署目标')
@click.option('--commands', '-cmd', multiple=True, help='要执行的命令')
@click.pass_context
def deploy(ctx, target, commands):
    """执行部署操作"""
    kos = ctx.obj['kos']
    commands_list = list(commands) if commands else None
    
    click.echo(f"🚀 开始部署流程...")
    success = kos.deploy(target=target, commands=commands_list)
    
    if success:
        click.echo("✅ 部署成功!")
        sys.exit(0)
    else:
        click.echo("❌ 部署失败!", err=True)
        sys.exit(1)


@main.command()
@click.option('--script', '-s', type=click.Path(exists=True), help='要执行的脚本路径')
@click.pass_context
def launch(ctx, script):
    """启动/发射代码"""
    kos = ctx.obj['kos']
    
    click.echo(f"🚀 开始启动流程...")
    success = kos.launch(script=script)
    
    if success:
        click.echo("✅ 启动成功!")
        sys.exit(0)
    else:
        click.echo("❌ 启动失败!", err=True)
        sys.exit(1)


@main.command()
@click.pass_context
def status(ctx):
    """显示当前状态"""
    kos = ctx.obj['kos']
    status_info = kos.status()
    
    click.echo("📊 KOS 状态信息:")
    click.echo(f"  版本: {status_info['version']}")
    click.echo(f"  部署类型: {status_info['deployment_type']}")
    click.echo(f"  目标: {status_info['target']}")
    click.echo(f"  自动启动: {'是' if status_info['auto_start'] else '否'}")


@main.command()
@click.argument('key')
@click.argument('value', required=False)
@click.option('--config-file', '-c', type=click.Path(), help='配置文件路径')
@click.pass_context
def config(ctx, key, value, config_file):
    """
    查看或设置配置项
    
    示例:
        kos config deployment.target        # 查看配置
        kos config deployment.target prod   # 设置配置
    """
    cfg = ctx.obj['config']
    
    if value is None:
        # 查看配置
        val = cfg.get(key)
        if val is not None:
            click.echo(f"{key} = {val}")
        else:
            click.echo(f"配置项 '{key}' 不存在", err=True)
    else:
        # 设置配置
        cfg.set(key, value)
        if config_file:
            cfg.save(config_file)
            click.echo(f"✅ 配置已保存到 {config_file}")
        else:
            click.echo(f"✅ 配置已设置: {key} = {value}")
            click.echo("   (注意: 未保存到文件)")


@main.command()
@click.argument('output', type=click.Path(), default='kos-config.yaml')
@click.pass_context
def init(ctx, output):
    """
    初始化配置文件
    
    创建一个默认的配置文件模板。
    """
    cfg = Config()
    cfg.save(output)
    click.echo(f"✅ 配置文件已创建: {output}")


if __name__ == '__main__':
    main()
