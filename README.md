# KOS - 自动发射代码工具

KOS (Kubernetes Operations System / 自动发射代码) 是一个用于自动部署和发射代码的命令行工具。

## 功能特性

- 🚀 自动化部署流程
- ⚙️ 灵活的配置管理
- 📝 详细的日志记录
- 🎯 支持多目标部署
- 💻 简单易用的命令行界面

## 安装

### 从源码安装

```bash
git clone https://github.com/Liujunmin0930/kos.git
cd kos
pip install -e .
```

### 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 初始化配置

```bash
kos init
```

这将创建一个默认的配置文件 `kos-config.yaml`。

### 2. 查看状态

```bash
kos status
```

### 3. 执行部署

```bash
kos deploy
```

指定目标部署：

```bash
kos deploy --target production
```

执行自定义命令：

```bash
kos deploy --commands "echo 'Step 1'" --commands "echo 'Step 2'"
```

### 4. 启动代码

```bash
kos launch
```

指定脚本启动：

```bash
kos launch --script /path/to/script.py
```

## 配置

### 配置文件格式

配置文件使用 YAML 格式：

```yaml
name: kos
version: 0.1.0
deployment:
  type: default
  target: local
  auto_start: false
logging:
  level: INFO
  file: null
```

### 配置管理

查看配置项：

```bash
kos config deployment.target
```

设置配置项：

```bash
kos config deployment.target production
```

保存配置到文件：

```bash
kos config deployment.target production --config-file kos-config.yaml
```

## 命令行选项

### 全局选项

- `--config, -c`: 指定配置文件路径
- `--version`: 显示版本信息
- `--help`: 显示帮助信息

### deploy 命令

执行部署操作。

```bash
kos deploy [OPTIONS]
```

选项：
- `--target, -t`: 部署目标
- `--commands, -cmd`: 要执行的命令（可多次使用）

### launch 命令

启动/发射代码。

```bash
kos launch [OPTIONS]
```

选项：
- `--script, -s`: 要执行的脚本路径

### status 命令

显示当前状态信息。

```bash
kos status
```

### config 命令

查看或设置配置项。

```bash
kos config KEY [VALUE] [OPTIONS]
```

选项：
- `--config-file, -c`: 配置文件路径

### init 命令

初始化配置文件。

```bash
kos init [OUTPUT]
```

## 使用示例

### 示例1: 本地部署

```bash
# 初始化配置
kos init my-config.yaml

# 使用配置文件部署
kos --config my-config.yaml deploy
```

### 示例2: 自定义部署流程

```bash
kos deploy \
  --target production \
  --commands "git pull origin main" \
  --commands "npm install" \
  --commands "npm run build" \
  --commands "npm start"
```

### 示例3: 启动Python脚本

```bash
kos launch --script deploy.py
```

## 开发

### 项目结构

```
kos/
├── kos/
│   ├── __init__.py      # 包初始化
│   ├── cli.py           # 命令行接口
│   ├── core.py          # 核心功能
│   └── config.py        # 配置管理
├── setup.py             # 安装配置
├── requirements.txt     # 依赖列表
└── README.md           # 说明文档
```

### 运行测试

```bash
python -m pytest tests/
```

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求！
