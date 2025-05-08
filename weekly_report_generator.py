#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
智能周报生成器
功能：从模板文件中读取并替换占位符，生成个性化周报
作者：Your Name
日期：2024年
"""

import argparse
import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys
from pathlib import Path
try:
    import markdown  # 用于将Markdown转换为HTML
    from weasyprint import HTML  # 用于生成PDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

class WeeklyReportGenerator:
    def __init__(self):
        # 初始化配置
        self.config = self.load_config()
        self.script_dir = Path(__file__).parent.absolute()
        
        # 确保必要的目录存在
        self.ensure_directories()
        
        # 加载用户配置
        self.username = self.get_username()
        self.history = self.load_history()

    def load_config(self) -> Dict:
        """加载配置文件"""
        config_path = Path(__file__).parent / "config.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"警告：加载配置文件失败：{str(e)}")
            # 返回默认配置
            return {
                "templates_dir": "templates",
                "reports_dir": "reports",
                "history_file": "history.json",
                "file_format": ".txt",
                "date_format": "%Y-%m-%d",
                "default_encoding": "utf-8"
            }

    def ensure_directories(self):
        """确保必要的目录存在"""
        for dir_name in ["templates_dir", "reports_dir"]:
            dir_path = self.script_dir / self.config[dir_name]
            dir_path.mkdir(exist_ok=True)

    def get_username(self) -> str:
        """获取或设置用户名"""
        config_file = self.script_dir / "user_config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)["username"]
            except:
                pass
        
        username = input("请输入您的姓名（首次使用需要设置）：").strip()
        while not username:
            username = input("姓名不能为空，请重新输入：").strip()
        
        # 保存用户配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump({"username": username}, f, ensure_ascii=False, indent=2)
        
        return username

    def load_history(self) -> Dict:
        """加载历史记录"""
        history_path = self.script_dir / self.config["history_file"]
        if history_path.exists():
            try:
                with open(history_path, 'r', encoding=self.config['default_encoding']) as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告：读取历史记录失败：{str(e)}")
                return {}
        return {}

    def save_history(self, data: Dict, template_name: str) -> None:
        """保存历史记录"""
        history_key = f"{self.username}_{Path(template_name).stem}"
        self.history[history_key] = {
            "last_updated": datetime.now().strftime(self.config["date_format"]),
            "data": data
        }
        
        history_path = self.script_dir / self.config["history_file"]
        try:
            with open(history_path, 'w', encoding=self.config['default_encoding']) as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"警告：保存历史记录失败：{str(e)}")

    def list_templates(self) -> List[Tuple[str, str, str]]:
        """列出所有可用的模板"""
        templates_dir = self.script_dir / self.config["templates_dir"]
        templates = []
        
        for template_type, settings in self.config["template_settings"].items():
            template_path = templates_dir / settings["default_template"]
            if template_path.exists():
                templates.append((
                    str(template_path),
                    settings["name"],
                    settings["description"]
                ))
        
        return templates

    def preview_template(self, template_path: str) -> Optional[str]:
        """预览模板内容"""
        try:
            with open(template_path, 'r', encoding=self.config['default_encoding']) as f:
                content = f.read()
            
            separator = self.config["ui_settings"]["preview_separator"] * 50
            print(f"\n{separator}")
            print("模板预览".center(50))
            print(separator)
            print(content)
            print(separator)
            
            while True:
                choice = input("\n是否使用该模板？(y/n): ").lower().strip()
                if choice == 'n':
                    return None
                elif choice == 'y':
                    return template_path
                print("请输入 y 或 n")
        except Exception as e:
            print(f"预览模板失败：{str(e)}")
            return None

    def select_template(self) -> str:
        """让用户选择模板"""
        templates = self.list_templates()
        if not templates:
            print("错误：未找到任何模板！")
            sys.exit(1)
        
        while True:
            print("\n可用的模板：")
            for i, (_, name, desc) in enumerate(templates, 1):
                print(f"{i}. {name}")
                print(f"   说明：{desc}")
            
            try:
                choice = int(input("\n请选择模板编号（输入数字）："))
                if 1 <= choice <= len(templates):
                    template_path = templates[choice-1][0]
                    result = self.preview_template(template_path)
                    if result:
                        return result
                    continue
            except ValueError:
                pass
            print("无效的选择，请重试。")

    def get_auto_fill_data(self) -> Dict[str, str]:
        """获取自动填充数据"""
        now = datetime.now()
        week_number = int(now.strftime("%W"))
        
        return {
            "日期": now.strftime("%Y年%m月%d日"),
            "周次": f"第{week_number}周",
            "姓名": self.username
        }

    def get_user_input(self, placeholders: List[str], template_name: str) -> Dict[str, str]:
        """获取用户输入"""
        user_data = {}
        auto_fill = self.get_auto_fill_data()
        
        for placeholder in placeholders:
            # 自动填充字段
            if placeholder in auto_fill:
                user_data[placeholder] = auto_fill[placeholder]
                print(f"自动填充 {placeholder}：{auto_fill[placeholder]}")
                continue
            
            # 获取历史记录
            history_key = f"{self.username}_{Path(template_name).stem}"
            last_input = None
            if history_key in self.history:
                last_input = self.history[history_key]["data"].get(placeholder)
            
            prompt = f"请输入{placeholder}"
            if last_input:
                prompt += f"（上次输入：{last_input}，直接回车使用上次输入）"
            prompt += "："
            
            while True:
                value = input(prompt).strip()
                if not value and last_input:
                    value = last_input
                if value:
                    user_data[placeholder] = value
                    break
                else:
                    print(f"错误：{placeholder} 不能为空！")
        
        # 保存非自动填充的数据到历史记录
        manual_input = {k: v for k, v in user_data.items() if k not in auto_fill}
        self.save_history(manual_input, template_name)
        
        return user_data

    def extract_placeholders(self, template_path: str) -> List[str]:
        """提取模板中的占位符"""
        try:
            with open(template_path, 'r', encoding=self.config['default_encoding']) as f:
                content = f.read()
            return list(set(re.findall(r'{{(.*?)}}', content)))
        except Exception as e:
            print(f"读取模板失败：{str(e)}")
            sys.exit(1)

    def export_to_pdf(self, markdown_content: str, output_path: str) -> bool:
        """
        将Markdown内容转换为PDF
        参数：
            markdown_content: Markdown格式的内容
            output_path: 输出PDF文件路径
        返回：
            是否成功导出
        """
        if not PDF_SUPPORT:
            print("警告：未安装PDF导出所需的依赖包。")
            print("请运行：pip install markdown weasyprint")
            return False

        try:
            # 转换Markdown为HTML
            html_content = markdown.markdown(
                markdown_content,
                extensions=['extra', 'tables', 'toc']
            )

            # 添加基本的CSS样式
            styled_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; }}
                    h2 {{ color: #34495e; margin-top: 20px; }}
                    .section {{ margin: 15px 0; padding: 10px; background: #f9f9f9; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            # 生成PDF
            HTML(string=styled_html).write_pdf(output_path)
            print(f"已生成PDF文件：{output_path}")
            return True
        except Exception as e:
            print(f"生成PDF时出错：{str(e)}")
            return False

    def generate_report(self, template_path: str, user_data: Dict[str, str], output_path: str) -> None:
        """生成报告"""
        try:
            # 读取模板
            with open(template_path, 'r', encoding=self.config['default_encoding']) as f:
                template_content = f.read()
            
            # 替换占位符
            for key, value in user_data.items():
                template_content = template_content.replace(f"{{{{{key}}}}}", value)
            
            # 保存生成的报告
            with open(output_path, 'w', encoding=self.config['default_encoding']) as f:
                f.write(template_content)
            
            print(f"\n成功生成周报：{output_path}")

            # 如果配置中启用了PDF导出，同时生成PDF版本
            if self.config.get("export_pdf", False):
                pdf_path = output_path.rsplit('.', 1)[0] + '.pdf'
                if self.export_to_pdf(template_content, pdf_path):
                    print(f"同时生成了PDF版本：{pdf_path}")

        except Exception as e:
            print(f"生成报告失败：{str(e)}")
            sys.exit(1)

    def get_default_filename(self) -> str:
        """生成默认的输出文件名"""
        now = datetime.now()
        return f"{self.username}_周报_{now.strftime('%Y%m%d')}{self.config['file_format']}"

    def run(self):
        """运行周报生成器"""
        # 解析命令行参数
        parser = argparse.ArgumentParser(description="智能周报生成器")
        parser.add_argument("--template", help="周报模板文件路径")
        parser.add_argument("--output", help="生成的周报文件路径")
        parser.add_argument("--pdf", action="store_true", help="同时生成PDF格式")
        args = parser.parse_args()
        
        # 如果命令行指定了PDF导出，临时启用PDF导出功能
        if args.pdf:
            self.config["export_pdf"] = True
        
        # 选择模板
        template_path = args.template if args.template else self.select_template()
        
        # 设置输出路径
        if not args.output:
            reports_dir = self.script_dir / self.config["reports_dir"]
            output_path = reports_dir / self.get_default_filename()
        else:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 提取占位符并获取用户输入
        placeholders = self.extract_placeholders(template_path)
        user_data = self.get_user_input(placeholders, template_path)
        
        # 生成报告
        self.generate_report(template_path, user_data, str(output_path))

def main():
    generator = WeeklyReportGenerator()
    generator.run()

if __name__ == "__main__":
    main() 