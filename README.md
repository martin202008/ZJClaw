# ZJClaw 

<div align="center">
  <p>
    <img src="https://img.shields.io/badge/version-0.1.5-blue" alt="Version">
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  </p>
</div>

**ZJClaw** 是宗靖商管开发的商业地产智能管理助手，专注于商业招商、商业运营、数字营销、工程物管、财务管理和人事行政等核心业务领域。

## 公司信息

- **公司**：宗靖商管
- **定位**：城市商业服务运营商创新者
- **使命**：数字化技术+精细化运营，为商业资产注入可持续活力

## 核心能力

| 模块 | 能力描述 |
|------|----------|
| **商业招商** | 品牌定位、租户评估、招商谈判、合同管理 |
| **商业运营** | 运营标准、巡场管理、客户服务、经营分析 |
| **数字营销** | 私域运营、社媒营销、数据分析、会员管理 |
| **工程物管** | 设备管理、安全管理、能耗管控、装修审批 |
| **财务管理** | 预算管理、成本分析、收入管理、风险控制 |
| **人事行政** | 招聘培训、绩效考核、薪酬管理、行政事务 |

## 快速开始

### WebUI 启动

```bash
cd webui
python standalone_app.py
```

然后访问 http://localhost:5000

### 配置

1. 首次使用请在「配置」→「AI 设置」中配置 MiniMax API Key
2. 可选：在「配置」→「工作区设置」中设置安全沙箱目录

### 安装依赖

```bash
pip install -e .
```

## 系统技能

| 技能 | 功能 |
|------|------|
| **find-skills** | 搜索和安装新技能 |
| **multi-search-engine** | 多搜索引擎集成 |
| **automation-workflows** | 自动化工作流设计 |

## 项目结构

```
zjclaw/
├── agent/              # 核心代理逻辑
│   ├── loop.py        # Agent循环
│   ├── context.py     # 提示词构建
│   ├── memory.py      # 持久化记忆
│   ├── skills.py      # 技能加载器
│   └── tools/         # 工具集
├── skills/            # 内置技能
│   ├── recruitment/   # 商业招商
│   ├── operations/    # 商业运营
│   ├── marketing/     # 数字营销
│   ├── engineering/   # 工程物管
│   ├── finance/       # 财务管理
│   └── hr/            # 人事行政
├── providers/         # LLM提供商
├── templates/         # 模板文件
│   ├── SOUL.md        # 角色定义
│   └── AGENTS.md      # 智能体指令
└── utils/            # 工具函数

skills/
├── system-skills/    # 系统技能
│   ├── find-skills/
│   ├── multi-search-engine/
│   └── automation-workflows/
└── user-skills/      # 用户技能（可选）

webui/
├── standalone_app.py  # Web服务
└── templates/        # 前端页面
```

## 自动更新

ZJClaw 支持一键自动更新功能：

1. 在「版本」页面点击「检查更新」
2. 如有新版本，点击「一键更新」按钮
3. 重启应用完成更新

## 开发指南

### 添加自定义技能

将技能放入 `skills/user-skills/` 目录，技能格式：

```
skills/user-skills/my-skill/
├── SKILL.md           # 技能说明
└── _meta.json        # 技能元数据
```

### 修改角色配置

编辑 `zjclaw/templates/SOUL.md` 可自定义 ZJClaw 的角色定位。

## 许可证

MIT License

## 联系方式

- **开发公司**：苏州涣葆宗靖商业运营管理有限公司
- **负责人**：兴哥
- **网址**：www.zjclaw.com
