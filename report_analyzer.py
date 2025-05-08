#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
周报分析器
功能：分析周报内容，生成统计信息和可视化图表
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
import jieba  # 用于中文分词
from datetime import datetime
try:
    import matplotlib.pyplot as plt
    import numpy as np
    PLOT_SUPPORT = True
except ImportError:
    PLOT_SUPPORT = False

class ReportAnalyzer:
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.reports_dir = Path(self.config["reports_dir"])
        self.stats_dir = Path("statistics")
        self.stats_dir.mkdir(exist_ok=True)

    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败：{str(e)}")
            return {}

    def analyze_word_frequency(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """分析文本中词语出现频率"""
        # 使用结巴分词
        words = jieba.cut(text)
        # 过滤停用词
        stop_words = {'的', '了', '和', '是', '就', '都', '而', '及', '与', '着'}
        words = [w for w in words if len(w) > 1 and w not in stop_words]
        # 统计词频
        counter = Counter(words)
        return counter.most_common(top_n)

    def generate_word_cloud(self, text: str, output_path: str) -> None:
        """生成词云图"""
        if not PLOT_SUPPORT:
            print("警告：未安装matplotlib，无法生成词云图")
            return

        try:
            from wordcloud import WordCloud
            # 生成词云
            wc = WordCloud(font_path="msyh.ttc",  # 使用微软雅黑字体
                         width=800,
                         height=400,
                         background_color='white')
            wc.generate(text)
            
            # 保存词云图
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.savefig(output_path)
            plt.close()
        except ImportError:
            print("警告：未安装wordcloud，无法生成词云图")
            print("请运行：pip install wordcloud")

    def analyze_report(self, report_path: str) -> Dict:
        """分析单个报告"""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 基础统计
            stats = {
                "字数": len(content),
                "段落数": len(content.split('\n\n')),
                "行数": len(content.splitlines())
            }

            # 词频分析
            word_freq = self.analyze_word_frequency(content)
            stats["高频词"] = dict(word_freq)

            return stats
        except Exception as e:
            print(f"分析报告失败：{str(e)}")
            return {}

    def generate_trend_chart(self, data: List[Tuple[str, int]], output_path: str) -> None:
        """生成趋势图表"""
        if not PLOT_SUPPORT:
            print("警告：未安装matplotlib，无法生成趋势图")
            return

        dates, values = zip(*data)
        plt.figure(figsize=(12, 6))
        plt.plot(dates, values, marker='o')
        plt.title("周报数据趋势")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def analyze_all_reports(self) -> Dict:
        """分析所有报告并生成统计报告"""
        all_stats = {
            "总体统计": {
                "报告总数": 0,
                "总字数": 0,
                "平均字数": 0
            },
            "趋势分析": [],
            "词频统计": Counter()
        }

        # 遍历所有报告文件
        for report_file in self.reports_dir.glob("*.txt"):
            stats = self.analyze_report(str(report_file))
            if not stats:
                continue

            # 更新总体统计
            all_stats["总体统计"]["报告总数"] += 1
            all_stats["总体统计"]["总字数"] += stats["字数"]
            
            # 记录趋势数据
            date_str = report_file.stem.split('_')[-1]
            all_stats["趋势分析"].append((date_str, stats["字数"]))
            
            # 更新词频统计
            for word, freq in stats["高频词"].items():
                all_stats["词频统计"][word] += freq

        # 计算平均值
        if all_stats["总体统计"]["报告总数"] > 0:
            all_stats["总体统计"]["平均字数"] = (
                all_stats["总体统计"]["总字数"] / 
                all_stats["总体统计"]["报告总数"]
            )

        # 生成可视化图表
        if PLOT_SUPPORT:
            # 生成趋势图
            self.generate_trend_chart(
                sorted(all_stats["趋势分析"]),
                self.stats_dir / "trend_chart.png"
            )
            
            # 生成词云图
            text = " ".join(word * freq for word, freq in all_stats["词频统计"].items())
            self.generate_word_cloud(text, self.stats_dir / "word_cloud.png")

        return all_stats

    def generate_report(self) -> None:
        """生成分析报告"""
        stats = self.analyze_all_reports()
        
        # 生成报告文本
        report = f"""# 周报分析报告
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 总体统计
- 报告总数：{stats['总体统计']['报告总数']}
- 总字数：{stats['总体统计']['总字数']}
- 平均字数：{stats['总体统计']['平均字数']:.2f}

## 高频词汇（Top 10）
"""
        for word, freq in stats["词频统计"].most_common(10):
            report += f"- {word}: {freq}次\n"

        report += """
## 可视化图表
1. 字数趋势图：statistics/trend_chart.png
2. 词云图：statistics/word_cloud.png

## 分析结论
1. 字数趋势显示了报告的详细程度变化
2. 高频词反映了工作/学习的重点领域
3. 可视化图表直观展示了报告质量变化
"""

        # 保存报告
        output_path = self.stats_dir / f"analysis_report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n分析报告已生成：{output_path}")
        print("提示：查看报告中的可视化图表以获取更直观的分析结果")

def main():
    analyzer = ReportAnalyzer()
    analyzer.generate_report()

if __name__ == "__main__":
    main() 