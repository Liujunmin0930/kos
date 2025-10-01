# kos

自动发射代码 (Automatic Code Launcher)

kos 是一个简单的自动化代码执行工具，可以通过配置文件管理和执行多个脚本或命令。

kos is a simple automation tool for executing code and scripts through configuration management.

## 功能特性 (Features)

- 📝 基于 JSON 的配置文件 (JSON-based configuration)
- 🎯 支持多个目标配置 (Multiple target configurations)
- 🌍 环境变量支持 (Environment variable support)
- 📂 自定义工作目录 (Custom working directories)
- 🚀 一键执行 (One-command execution)

## 安装 (Installation)

确保系统已安装 Python 3.6 或更高版本。

Make sure Python 3.6 or higher is installed.

```bash
git clone https://github.com/Liujunmin0930/kos.git
cd kos
chmod +x kos.py
```

## 使用方法 (Usage)

### 1. 查看帮助 (View help)

```bash
python3 kos.py --help
```

### 2. 列出所有目标 (List all targets)

```bash
python3 kos.py --list
```

### 3. 执行默认目标 (Execute default target)

```bash
python3 kos.py
```

### 4. 执行指定目标 (Execute specific target)

```bash
python3 kos.py hello
python3 kos.py python_example
```

### 5. 使用自定义配置文件 (Use custom config file)

```bash
python3 kos.py --config my_config.json my_target
```

## 配置示例 (Configuration Example)

创建或编辑 `config.json` 文件 (Create or edit `config.json`):

```json
{
  "default_target": "hello",
  "targets": {
    "hello": {
      "command": "echo '你好，世界！'",
      "working_dir": ".",
      "env": {}
    },
    "run_tests": {
      "command": "python3 -m pytest tests/",
      "working_dir": ".",
      "env": {
        "PYTHONPATH": "."
      }
    },
    "build": {
      "command": "python3 setup.py build",
      "working_dir": ".",
      "env": {}
    }
  }
}
```

### 配置说明 (Configuration Parameters)

- `default_target`: 默认执行的目标名称 (Default target name)
- `targets`: 目标配置字典 (Target configurations dictionary)
  - `command`: 要执行的命令 (Command to execute)
  - `working_dir`: 工作目录，默认为当前目录 (Working directory, defaults to current)
  - `env`: 额外的环境变量 (Additional environment variables)

## 示例场景 (Example Use Cases)

- 🧪 自动运行测试 (Automated test execution)
- 🔨 构建项目 (Project building)
- 🚀 部署应用 (Application deployment)
- 🔄 定时任务 (Scheduled tasks)
- 📊 数据处理脚本 (Data processing scripts)

## 许可证 (License)

MIT
