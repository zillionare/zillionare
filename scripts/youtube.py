"""给 youtube 视频加中文字幕

自动化流程：切分 -> 翻译 -> 合并

用法：
python /path/to/youtube.py /path/to/file.srt [end_time] [max_workers]
"""

import time
import random
from pathlib import Path
import re
import os
import sys
import threading
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

proxy = "http://127.0.0.1:7890"

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

# 然后再导入和使用 Translator
try:
    from googletrans import Translator
except ImportError:
    print("警告: googletrans库未安装。请运行 'pip install googletrans' 安装。")
    Translator = None

# 创建线程锁，确保线程安全
translator_lock = threading.Lock()

def translate_text_batch(texts: list, target_lang='zh-cn') -> list:
    """使用googletrans批量翻译文本列表，通过环境变量使用代理"""
    if Translator is None:
        raise ImportError("googletrans库未安装。请运行 'pip install googletrans==4.0.0-rc1' 安装。")
    
    try:
        # 使用线程锁确保线程安全
        with translator_lock:
            # 简化创建翻译器实例，不再传递代理参数
            translator = Translator()
            
            # 批量翻译，只需要一次延迟
            time.sleep(random.uniform(0.5, 1.0))  # 对于一次大的请求，适当的延迟
            results = translator.translate(texts, dest=target_lang)
            
            # 检查是否是协程对象
            import inspect
            if inspect.iscoroutine(results):
                # 如果是协程，需要使用asyncio运行
                import asyncio
                results = asyncio.run(results)
            
            # 提取翻译结果文本
            translated_texts = []
            for result in results:
                translated_texts.append(result.text)
                
        return translated_texts
    except Exception as e:
        print(f"批量翻译失败: {e}，将返回原文")
        return texts

def translate_srt_file_threaded(file_path: str, output_path: str = None):
    """线程安全的翻译单个SRT文件"""
    # 为每个线程设置独立的环境变量
    thread_id = threading.current_thread().ident
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    
    # 调用原有的翻译函数
    return translate_srt_file(file_path, output_path)

def split_srt(path: str, end_time: str = None):
    """将SRT文件切分为多个小文件，使用系统临时目录"""
    file = Path(path).expanduser()
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    timestamps = ["00:00:00.000"]
    texts = []  # 存储对应的文本内容
    for i in range(len(lines)):
        # 匹配 mm:ss - 格式的时间戳行
        time_match = re.match(r"^(\d+):(\d+)(\s*-\s*)?", lines[i])
        if time_match:
            # 提取分和秒
            mm = int(time_match.group(1))
            ss = int(time_match.group(2))
            # 转换为标准时间戳格式
            timestamps.append(f"00:{mm:02d}:{ss:02d}.000")
            
            # 提取文本内容（时间戳后面的部分）
            text_content = lines[i][time_match.end():].strip()
            texts.append(text_content)
    
    # 处理结束时间
    if end_time is not None:
        timestamps.append(end_time)
    else:
        # 确保至少有两个时间戳
        if len(timestamps) > 1:
            # 计算最后一个片段的结束时间（假设每个片段持续约3秒）
            last_time = timestamps[-1]
            hh, mm, ss_ms = last_time.split(":")
            # 修复：转换为整数进行计算
            hh_int = int(hh)
            mm_int = int(mm)
            ss = int(ss_ms.split(".")[0]) + 3
            
            if ss >= 60:
                mm_int += 1
                ss = ss % 60
                if mm_int >= 60:
                    hh_int += 1
                    mm_int = mm_int % 60
            
            # 使用整数进行格式化
            timestamps.append(f"{hh_int:02d}:{mm_int:02d}:{ss:02d}.000")
    
    # 使用系统临时目录，而不是与输入文件同级的目录
    temp_dir = tempfile.mkdtemp(prefix="srt_split_")
    output_dir = Path(temp_dir)
    
    # 生成SRT文件
    m = 1  # 文件计数器
    buffer = []
    
    # 确保texts和timestamps-1的长度匹配
    texts = texts[:len(timestamps)-1]
    
    for j in range(len(texts)):
        # 添加字幕序号、时间戳和文本
        buffer.append(f"{j+1}\n")
        buffer.append(f"{timestamps[j]} --> {timestamps[j+1]}\n")
        buffer.append(f"{texts[j]}\n\n")
        
        # 当缓冲区达到一定大小时，写入文件
        if len(buffer) > 200:  # 约50个字幕条目
            to = output_dir / f"{m:02d}.srt"
            with open(to, "w", encoding="utf-8") as f:
                f.writelines(buffer)
            buffer = []
            m += 1
    
    # 写入剩余内容
    if len(buffer) > 0:
        to = output_dir / f"{m:02d}.srt"
        with open(to, "w", encoding="utf-8") as f:
            f.writelines(buffer)
    
    return output_dir

def translate_srt_file(file_path: str, output_path: str = None):
    """翻译单个SRT文件，使用googletrans原生批量翻译功能"""
    file = Path(file_path).expanduser()
    
    if output_path is None:
        # 默认输出为原文件名加-translated后缀
        output_path = file.parent / f"{file.stem}-translated{file.suffix}"
    else:
        output_path = Path(output_path).expanduser()
    
    if proxy:
        print(f"使用代理: {proxy}")
    
    print(f"开始翻译文件: {file}")
    
    # 1. 提取所有文本行和保留原始结构信息
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 用于存储原始结构和需要翻译的文本
    subtitle_entries = []
    texts_to_translate = []
    
    i = 0
    while i < len(lines):
        # 检查是否是字幕序号行
        if lines[i].strip().isdigit():
            entry = {
                'index_line': lines[i],
                'timecode_line': '',
                'text_lines': [],
                'empty_line': ''
            }
            subtitle_entries.append(entry)
            
            i += 1
            # 保存时间戳行
            if i < len(lines) and '-->' in lines[i]:
                entry['timecode_line'] = lines[i]
                i += 1
            
            # 保存文本行
            while i < len(lines) and lines[i].strip():
                text_line = lines[i].strip()
                entry['text_lines'].append(text_line)
                texts_to_translate.append(text_line)
                i += 1
            
            # 保存空行（如果有）
            if i < len(lines) and not lines[i].strip():
                entry['empty_line'] = lines[i]
        i += 1
    
    # 2. 使用googletrans原生批量翻译功能
    print(f"开始批量翻译 {len(texts_to_translate)} 个文本片段...")
    translated_texts = translate_text_batch(texts_to_translate)
    
    # 3. 还原SRT结构
    translated_lines = []
    text_index = 0
    
    for entry in subtitle_entries:
        # 添加序号行
        translated_lines.append(entry['index_line'])
        # 添加时间戳行
        translated_lines.append(entry['timecode_line'])
        
        # 添加翻译后的文本行
        for _ in entry['text_lines']:
            if text_index < len(translated_texts):
                translated_lines.append(translated_texts[text_index] + '\n')
            else:
                # 如果翻译结果不完整，使用原文（如果有）
                if entry['text_lines']:
                    translated_lines.append(entry['text_lines'][0] + '\n')
            text_index += 1
        
        # 添加空行
        translated_lines.append(entry['empty_line'])
    
    # 4. 写入翻译后的文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(translated_lines)
    
    print(f"翻译完成，输出文件: {output_path}")
    return output_path

def translate_dir(dir_path: str, max_workers: int = 4):
    """翻译目录中的所有SRT文件，使用多线程并行处理"""
    directory = Path(dir_path).expanduser()
    srt_files = list(directory.glob("*.srt"))
    
    # 过滤掉已翻译的文件
    files_to_translate = [f for f in srt_files if "-translated" not in f.name]
    
    print(f"找到 {len(srt_files)} 个SRT文件，其中 {len(files_to_translate)} 个需要翻译")
    
    # 使用线程池并行翻译文件
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有翻译任务
        future_to_file = {
            executor.submit(translate_srt_file_threaded, str(srt_file)): srt_file 
            for srt_file in files_to_translate
        }
        
        # 处理完成的任务
        for future in as_completed(future_to_file):
            srt_file = future_to_file[future]
            try:
                future.result()  # 获取结果，如果有异常会抛出
                print(f"完成翻译: {srt_file}")
            except Exception as e:
                print(f"翻译文件 {srt_file} 时出错: {e}")

def merge_srt(folder: str):
    """将翻译后的SRT文件合并为一个文件"""
    buffers = []
    folder_path = Path(folder).expanduser()
    
    # 获取所有翻译后的文件
    translated_files = sorted(folder_path.glob("*-translated.srt"))
    
    if not translated_files:
        print("未找到翻译后的SRT文件")
        return None
    
    print(f"找到 {len(translated_files)} 个翻译后的SRT文件，开始合并...")
    
    for file in translated_files:
        print(f"处理文件: {file.name}")
        with open(file, "r", encoding="utf-8") as f:
            buffers.extend(f.readlines())

    # 重新编号字幕序号
    result_lines = []
    subtitle_index = 1
    
    i = 0
    while i < len(buffers):
        line = buffers[i]
        
        # 跳过空行
        if not line.strip():
            result_lines.append(line)
            i += 1
            continue
            
        # 处理序号行
        if line.strip().isdigit():
            result_lines.append(f"{subtitle_index}\n")
            i += 1
            
            # 添加时间戳行
            if i < len(buffers):
                result_lines.append(buffers[i])
                i += 1
                
            # 添加文本行
            while i < len(buffers) and buffers[i].strip():
                result_lines.append(buffers[i])
                i += 1
                
            # 添加空行
            if i < len(buffers) and not buffers[i].strip():
                result_lines.append(buffers[i])
                i += 1
                
            subtitle_index += 1
        else:
            i += 1
    
    # 写入合并后的文件到临时目录
    temp_dir = tempfile.mkdtemp(prefix="srt_merge_")
    output_file = Path(temp_dir) / "translated.srt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(result_lines)
    
    print(f"合并完成，输出文件: {output_file}")
    return output_file

def process_srt_file(file_path: str, end_time: str = None, max_workers: int = 4):
    """完整的SRT处理流程：切分 -> 翻译 -> 合并，使用系统临时目录"""
    print(f"开始处理SRT文件: {file_path}")
    
    # 获取输入文件的信息
    input_file = Path(file_path).expanduser()
    
    try:
        # 1. 切分SRT文件（使用系统临时目录）
        print("步骤1: 切分SRT文件...")
        srt_dir = split_srt(file_path, end_time)
        
        # 2. 翻译切分后的文件
        print("步骤2: 翻译SRT文件...")
        translate_dir(str(srt_dir), max_workers)
        
        # 3. 合并翻译后的文件（使用系统临时目录）
        print("步骤3: 合并翻译后的SRT文件...")
        temp_output_file = merge_srt(str(srt_dir))
        
        # 4. 将最终输出文件移动到输入文件的同级目录，使用正确的文件名
        if temp_output_file:
            final_output_file = input_file.parent / f"{input_file.stem}-translated{input_file.suffix}"
            
            # 移动文件到最终位置
            shutil.move(str(temp_output_file), str(final_output_file))
            
            print(f"处理完成！最终输出文件: {final_output_file}")
            
            # 清理临时目录
            try:
                if srt_dir.exists():
                    shutil.rmtree(str(srt_dir.parent))
                temp_dir = Path(temp_output_file).parent
                if temp_dir.exists():
                    shutil.rmtree(str(temp_dir))
            except Exception as e:
                print(f"清理临时目录时出错: {e}")
            
            return str(final_output_file)
        else:
            print("处理失败，未能生成输出文件")
            return None
            
    except Exception as e:
        print(f"处理过程中出错: {e}")
        return None

def main():
    """主函数，处理命令行参数"""
    if len(sys.argv) < 2:
        print("用法: python youtube.py <srt_file_path> [end_time] [max_workers]")
        print("示例: python youtube.py /path/to/file.srt 01:30:00.000 4")
        sys.exit(1)
    
    file_path = sys.argv[1]
    end_time = sys.argv[2] if len(sys.argv) > 2 else None
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    
    try:
        process_srt_file(file_path, end_time, max_workers)
    except Exception as e:
        print(f"处理过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
