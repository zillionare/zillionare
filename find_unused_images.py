#!/usr/bin/env python3
"""
分析 docs/articles/python/numpy&pandas 目录下的 markdown 文件，
找出未被引用的 PNG 图片文件并删除它们。
"""

import os
import re
import glob
from pathlib import Path
from typing import Set, List, Tuple

def find_markdown_files(base_dir: str) -> List[str]:
    """查找所有 markdown 文件"""
    pattern = os.path.join(base_dir, "**", "*.md")
    return glob.glob(pattern, recursive=True)

def find_png_files(base_dir: str) -> List[str]:
    """查找所有 PNG 文件"""
    pattern = os.path.join(base_dir, "**", "*.png")
    return glob.glob(pattern, recursive=True)

def extract_image_references(md_file: str) -> Set[str]:
    """从 markdown 文件中提取图片引用"""
    image_refs = set()
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 匹配 markdown 图片语法: ![alt](image.png) 或 ![alt](./image.png)
        md_pattern = r'!\[.*?\]\(([^)]+\.png)\)'
        matches = re.findall(md_pattern, content, re.IGNORECASE)
        
        # 匹配 HTML img 标签: <img src="image.png" ...>
        html_pattern = r'<img[^>]+src=["\']([^"\']+\.png)["\'][^>]*>'
        html_matches = re.findall(html_pattern, content, re.IGNORECASE)
        
        # 合并所有匹配结果
        all_matches = matches + html_matches
        
        # 处理相对路径
        md_dir = os.path.dirname(md_file)
        for match in all_matches:
            # 移除可能的 ./ 前缀
            clean_match = match.lstrip('./')
            # 构建完整路径
            full_path = os.path.join(md_dir, clean_match)
            # 标准化路径
            normalized_path = os.path.normpath(full_path)
            image_refs.add(normalized_path)
            
    except Exception as e:
        print(f"读取文件 {md_file} 时出错: {e}")
    
    return image_refs

def analyze_directory(base_dir: str) -> Tuple[List[str], Set[str]]:
    """分析目录，返回所有PNG文件和被引用的图片"""
    print(f"分析目录: {base_dir}")
    
    # 查找所有文件
    md_files = find_markdown_files(base_dir)
    png_files = find_png_files(base_dir)
    
    print(f"找到 {len(md_files)} 个 markdown 文件")
    print(f"找到 {len(png_files)} 个 PNG 文件")
    
    # 提取所有图片引用
    all_referenced_images = set()
    
    for md_file in md_files:
        print(f"分析文件: {md_file}")
        refs = extract_image_references(md_file)
        all_referenced_images.update(refs)
        if refs:
            print(f"  引用的图片: {refs}")
    
    print(f"\n总共引用了 {len(all_referenced_images)} 个图片")
    
    return png_files, all_referenced_images

def find_unused_images(png_files: List[str], referenced_images: Set[str]) -> List[str]:
    """找出未被引用的图片"""
    unused_images = []
    
    # 标准化所有PNG文件路径
    normalized_png_files = [os.path.normpath(f) for f in png_files]
    
    for png_file in normalized_png_files:
        if png_file not in referenced_images:
            unused_images.append(png_file)
    
    return unused_images

def main():
    base_dir = "docs/articles/python/numpy&pandas"
    
    if not os.path.exists(base_dir):
        print(f"目录不存在: {base_dir}")
        return
    
    # 分析目录
    png_files, referenced_images = analyze_directory(base_dir)
    
    # 找出未使用的图片
    unused_images = find_unused_images(png_files, referenced_images)
    
    print(f"\n{'='*50}")
    print(f"分析结果:")
    print(f"总PNG文件数: {len(png_files)}")
    print(f"被引用图片数: {len(referenced_images)}")
    print(f"未使用图片数: {len(unused_images)}")
    
    if unused_images:
        print(f"\n未被引用的图片文件:")
        for img in sorted(unused_images):
            print(f"  {img}")
        
        # 询问是否删除
        response = input(f"\n是否删除这 {len(unused_images)} 个未使用的图片文件? (y/N): ")
        if response.lower() in ['y', 'yes']:
            deleted_count = 0
            for img in unused_images:
                try:
                    os.remove(img)
                    print(f"已删除: {img}")
                    deleted_count += 1
                except Exception as e:
                    print(f"删除失败 {img}: {e}")
            print(f"\n成功删除 {deleted_count} 个文件")
        else:
            print("取消删除操作")
    else:
        print("\n没有找到未使用的图片文件")

if __name__ == "__main__":
    main()
