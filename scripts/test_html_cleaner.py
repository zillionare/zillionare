#!/usr/bin/env python3
"""
测试HTML清理功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helper import clean_html_content

def test_html_cleaner():
    """测试HTML清理功能"""
    
    # 测试用例1：正常的闭合标签
    test1 = "这是正常文本<div>内容</div>后面还有内容"
    result1 = clean_html_content(test1)
    print(f"测试1:\n原文: {test1}\n结果: {result1}\n")
    
    # 测试用例2：未闭合的标签
    test2 = "这是正常文本<div>内容<span>更多内容"
    result2 = clean_html_content(test2)
    print(f"测试2:\n原文: {test2}\n结果: {result2}\n")
    
    # 测试用例3：包含自闭合标签的情况
    test4 = "正常文本<img src='test.jpg'>继续文本<div>未闭合内容"
    result4 = clean_html_content(test4)
    print(f"测试4:\n原文: {test4}\n结果: {result4}\n")

if __name__ == "__main__":
    test_html_cleaner()