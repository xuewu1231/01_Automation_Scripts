# 智能周报生成器

一个简单易用的中文周报生成工具，支持多种模板和智能分析功能。

## 功能特点

### 1. 多样化模板

- 工作周报：适合日常工作汇报
- 学习周报：记录学习进度和心得
- 项目周报：项目管理和进度跟踪
- 个人总结：个人成长和能力提升
- 团队周报：团队管理和协作汇报

### 2. 智能功能

- 自动填充日期和周次
- 模板预览功能
- 历史记录管理
- 数据分析和可视化
- 自动保存和备份

### 3. 便捷特性

- 支持导出 PDF
- 中文分词统计
- 关键词提取
- 自定义提醒
- 数据备份恢复

## 使用说明

### 环境要求

- Python 3.7+
- 依赖包：见 requirements.txt

### 快速开始

1. 克隆仓库到本地

```bash
git clone https://github.com/你的用户名/weekly-report-generator.git
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 运行程序

- Windows 用户：双击运行 `生成周报.bat`
- 其他用户：

```bash
python weekly_report_generator.py
```

### 目录结构

```
weekly-report-generator/
├── weekly_report_generator.py  # 主程序
├── config.json                 # 配置文件
├── requirements.txt           # 依赖包列表
├── 生成周报.bat               # 快速启动脚本
├── templates/                # 模板目录
│   ├── work_report_template.md
│   ├── study_report_template.md
│   ├── project_report_template.md
│   ├── personal_summary_template.md
│   └── team_report_template.md
├── reports/                  # 生成的报告存放目录
└── backups/                 # 备份目录
```

### 配置说明

配置文件 `config.json` 包含以下主要设置：

- 模板设置：自定义不同类型的报告模板
- 界面设置：定制显示效果
- 分析设置：配置数据分析参数
- 提醒设置：自定义提醒时间和方式

## 常见问题

1. PDF 导出失败

- 确保已安装 weasyprint 依赖
- 检查系统是否支持中文字体

2. 提醒功能不工作

- 检查系统通知权限
- 确认配置文件中的提醒设置

3. 分析功能报错

- 确保已安装 jieba 和 matplotlib
- 检查报告文本是否满足最小字数要求

## 更新日志

### v1.3

- 新增多种报告模板
- 添加数据分析功能
- 优化用户界面
- 增加自动保存功能

### v1.2

- 添加 PDF 导出功能
- 实现数据备份
- 改进错误处理

### v1.1

- 添加模板预览
- 实现历史记录
- 优化文件管理

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License
