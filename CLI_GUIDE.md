# ZJClaw 命令行使用指南

## 目录

1. [基础命令](#1-基础命令)
2. [WebUI 命令](#2-webui-命令)
3. [智能体命令](#3-智能体命令)
4. [配置命令](#4-配置命令)
5. [技能命令](#5-技能命令)
6. [完整命令列表](#6-完整命令列表)

---

## 1. 基础命令

### 1.1 查看版本
```bash
zjclaw --version
```
显示当前 ZJClaw 版本号。

### 1.2 查看帮助
```bash
zjclaw --help
```
显示所有可用命令和选项。

---

## 2. WebUI 命令

### 2.1 启动 WebUI
```bash
zjclaw webui
```

可选参数：
- `--host <地址>` - 指定监听地址，默认 `0.0.0.0`
- `--port <端口>` - 指定端口，默认 `5000`
- `--debug` - 开启调试模式

**示例：**
```bash
zjclaw webui --port 8080
```

### 2.2 启动 WebUI（独立模式）
```bash
cd webui
python standalone_app.py
```

---

## 3. 智能体命令

### 3.1 启动智能体对话
```bash
zjclaw agent
```

启动交互式智能体对话模式，可以直接输入问题。

### 3.2 指定模型
```bash
zjclaw agent --model <模型名称>
```

**示例：**
```bash
zjclaw agent --model MiniMax-M2.7
```

### 3.3 指定提供商
```bash
zjclaw agent --provider <提供商>
```

常用提供商：
- `minimax` - MiniMax
- `openai` - OpenAI
- `deepseek` - DeepSeek
- `zhipu` - 智谱AI

### 3.4 单次对话
```bash
zjclaw agent "<你的问题>"
```

**示例：**
```bash
zjclaw agent "帮我制定甪直广场的年度招商计划"
```

---

## 4. 配置命令

### 4.1 初始化配置
```bash
zjclaw init
```

首次使用时运行，引导配置 API Key 和默认模型。

### 4.2 查看当前配置
```bash
zjclaw config show
```

显示当前的所有配置信息。

### 4.3 配置 API Key
```bash
zjclaw config set api.key <你的API_KEY>
```

**示例：**
```bash
zjclaw config set api.key eyJh...
```

### 4.4 配置默认模型
```bash
zjclaw config set model <模型名称>
```

**示例：**
```bash
zjclaw config set model MiniMax-M2.7
```

### 4.5 配置提供商
```bash
zjclaw config set provider <提供商>
```

**示例：**
```bash
zjclaw config set provider minimax
```

---

## 5. 技能命令

### 5.1 查看已安装技能
```bash
zjclaw skills list
```

列出所有已安装的技能模块。

### 5.2 查看技能详情
```bash
zjclaw skills show <技能名称>
```

**示例：**
```bash
zjclaw skills show recruitment
```

### 5.3 创建新技能
```bash
zjclaw skills create <技能名称>
```

在 `skills/user-skills/` 目录下创建新的技能模块。

---

## 6. 完整命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `zjclaw --version` | 显示版本 | `zjclaw --version` |
| `zjclaw --help` | 显示帮助 | `zjclaw --help` |
| `zjclaw webui` | 启动 WebUI | `zjclaw webui --port 8080` |
| `zjclaw agent` | 启动智能体 | `zjclaw agent --model MiniMax-M2.7` |
| `zjclaw init` | 初始化配置 | `zjclaw init` |
| `zjclaw config show` | 显示配置 | `zjclaw config show` |
| `zjclaw config set` | 设置配置 | `zjclaw config set model MiniMax-M2.7` |
| `zjclaw skills list` | 列出技能 | `zjclaw skills list` |
| `zjclaw skills show` | 查看技能 | `zjclaw skills show recruitment` |
| `zjclaw skills create` | 创建技能 | `zjclaw skills create my-skill` |
| `zjclaw doctor` | 诊断问题 | `zjclaw doctor` |
| `zjclaw info` | 显示信息 | `zjclaw info` |

---

## 常用场景

### 场景一：快速提问
```bash
zjclaw agent "分析本月运营数据"
```

### 场景二：启动 WebUI 并指定端口
```bash
zjclaw webui --port 5000 --host 0.0.0.0
```

### 场景三：更换模型
```bash
zjclaw agent --model MiniMax-M2.5
```

### 场景四：配置 MiniMax API
```bash
zjclaw config set provider minimax
zjclaw config set model MiniMax-M2.7
zjclaw config set api.key eyJh...
```

---

## 故障排除

### 问题：命令找不到
**解决：** 确保已正确安装 ZJClaw，并已将 Python Scripts 目录添加到 PATH。

### 问题：API Key 无效
**解决：** 检查配置中的 API Key 是否正确，或重新生成新的 Key。

### 问题：模型不支持
**解决：** 检查提供商是否支持该模型，参考提供商文档。

---

*更多信息请访问：https://github.com/martin202008/ZJClaw*
