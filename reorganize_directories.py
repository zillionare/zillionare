#!/usr/bin/env python3
"""
重新组织 docs/articles/python/numpy&pandas 目录结构：
- 如果子目录只包含一个 markdown 文件，将其移动到父目录下
- 删除空的子目录
"""

import os
import shutil
from pathlib import Path

def reorganize_directories(base_dir: str):
    """重新组织目录结构"""
    print(f"重新组织目录: {base_dir}")
    
    if not os.path.exists(base_dir):
        print(f"目录不存在: {base_dir}")
        return
    
    # 获取所有子目录
    subdirs = [d for d in os.listdir(base_dir) 
               if os.path.isdir(os.path.join(base_dir, d))]
    
    print(f"找到 {len(subdirs)} 个子目录")
    
    moved_files = []
    removed_dirs = []
    
    for subdir in subdirs:
        subdir_path = os.path.join(base_dir, subdir)
        
        # 获取子目录中的所有文件
        files = [f for f in os.listdir(subdir_path) 
                if os.path.isfile(os.path.join(subdir_path, f))]
        
        print(f"\n检查目录: {subdir}")
        print(f"  包含文件: {files}")
        
        # 如果只有一个文件且是 markdown 文件
        if len(files) == 1 and files[0].endswith('.md'):
            md_file = files[0]
            source_path = os.path.join(subdir_path, md_file)
            target_path = os.path.join(base_dir, md_file)
            
            try:
                # 移动文件
                shutil.move(source_path, target_path)
                print(f"  ✅ 移动文件: {md_file} -> {base_dir}/")
                moved_files.append((source_path, target_path))
                
                # 删除空目录
                os.rmdir(subdir_path)
                print(f"  ✅ 删除空目录: {subdir}")
                removed_dirs.append(subdir_path)
                
            except Exception as e:
                print(f"  ❌ 操作失败: {e}")
        else:
            print(f"  ⏭️  跳过 (包含 {len(files)} 个文件)")
    
    # 总结
    print(f"\n{'='*50}")
    print(f"重组完成:")
    print(f"移动的文件数: {len(moved_files)}")
    print(f"删除的目录数: {len(removed_dirs)}")
    
    if moved_files:
        print(f"\n移动的文件:")
        for source, target in moved_files:
            print(f"  {os.path.basename(source)}")
    
    if removed_dirs:
        print(f"\n删除的目录:")
        for dir_path in removed_dirs:
            print(f"  {os.path.basename(dir_path)}")

def main():
    base_dir = "docs/articles/python/numpy&pandas"
    
    # 询问用户确认
    print("此操作将:")
    print("1. 将只包含一个 markdown 文件的子目录中的文件移动到父目录")
    print("2. 删除空的子目录")
    print(f"3. 目标目录: {base_dir}")
    
    response = input("\n是否继续? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("操作已取消")
        return
    
    reorganize_directories(base_dir)

if __name__ == "__main__":
    main()
