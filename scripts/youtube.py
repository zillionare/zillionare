"""给 youtube 视频加中文字幕

自动化流程：切分 -> 翻译 -> 合并 -> 转SRT

用法：
python scripts/youtube.py /path/to/file.srt --splits 5
"""

import argparse
import inspect
import math
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List

from googletrans import Translator

# Set proxy
PROXY = "http://127.0.0.1:7890"
os.environ['HTTP_PROXY'] = PROXY
os.environ['HTTPS_PROXY'] = PROXY

def format_seconds_to_srt(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.000"

def translate_texts(texts: List[str], src='en', dest='zh-cn') -> List[str]:
    if not Translator:
        return texts
    
    translator = Translator()
    retries = 3
    for i in range(retries):
        try:
            time.sleep(random.uniform(0.5, 1.5))
            results = translator.translate(texts, src=src, dest=dest)
            
            if inspect.iscoroutine(results):
                import asyncio
                results = asyncio.run(results)
            
            if not isinstance(results, list):
                results = [results]
            
            translated_texts = [res.text for res in results]
            return translated_texts
        except Exception as e:
            print(f"Translation error (attempt {i+1}/{retries}): {type(e).__name__}: {e}")
            if i == retries - 1:
                return texts # Return original on failure
    return texts

class ScriptProcessor:
    def __init__(self, input_file: str, splits: int = 4):
        self.input_file = Path(input_file)
        self.splits = splits
        self.items = [] # {'time': seconds, 'text': str}

    def load_and_parse(self):
        if not self.input_file.exists():
            print(f"File not found: {self.input_file}")
            sys.exit(1)

        with open(self.input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Regex to match "mm:ss - text" or "mm:ss text"
        # max.srt format: "0:00 - Hi guys..."
        pattern = re.compile(r'^(\d+):(\d+)(?:\s*-\s*)?(.*)')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                mm = int(match.group(1))
                ss = int(match.group(2))
                text = match.group(3).strip()
                seconds = mm * 60 + ss
                self.items.append({'time': seconds, 'text': text})
        
        print(f"Parsed {len(self.items)} lines.")

    def process(self):
        if not self.items:
            print("No items parsed.")
            return

        # 1. Split
        total_items = len(self.items)
        # Ensure at least 1 split
        splits = max(1, self.splits)
        chunk_size = math.ceil(total_items / splits)
        chunks = []
        for i in range(0, total_items, chunk_size):
            chunks.append(self.items[i:i + chunk_size])

        # 2. Translate
        print(f"Splitting into {len(chunks)} chunks for translation...")
        
        def process_chunk(chunk_data):
            texts = [item['text'] for item in chunk_data]
            # 显式传递源语言和目标语言
            translated = translate_texts(texts, src='en', dest='zh-cn')
            for item, trans in zip(chunk_data, translated):
                # 强制覆盖原文本，或者你可以选择保留原文本
                # 这里我们直接用 translated 字段，如果翻译失败它本身就是原文本
                item['text_translated'] = trans
            return chunk_data

        results = []
        if len(chunks) == 1:
            results.append(process_chunk(chunks[0]))
        else:
            with ThreadPoolExecutor(max_workers=splits) as executor:
                futures = [executor.submit(process_chunk, chunk) for chunk in chunks]
                for f in futures:
                    results.append(f.result())

        # 3. Merge (implicitly done if we modify objects or flatten results)
        # Flatten results
        merged_items = []
        for res in results:
            merged_items.extend(res)
        
        # Sort by time to be safe (though chunks should preserve order if processed/extended correctly)
        # Note: results append order depends on future completion if we use as_completed, 
        # but here we iterated futures list which is in order of submission.
        # Ideally we should just concat chunks in order.
        # Since we iterated `futures` list created from `chunks` list, it is ordered.
        
        # 4. Convert to SRT
        srt_content = self.to_srt(merged_items)
        
        output_file = self.input_file.with_name(f"{self.input_file.stem}-translated.srt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        print(f"Output saved to {output_file}")

    def to_srt(self, items: List[Dict]) -> str:
        output = []
        for i, item in enumerate(items):
            start_time = item['time']
            # End time is next item's start time, or start + 2s for last item
            if i < len(items) - 1:
                end_time = items[i+1]['time']
            else:
                end_time = start_time + 2
            
            # Format
            start_str = format_seconds_to_srt(start_time)
            end_str = format_seconds_to_srt(end_time)
            
            text = item.get('text_translated', item['text'])
            
            output.append(f"{i+1}")
            output.append(f"{start_str} --> {end_str}")
            output.append(f"{text}\n")
        
        return "\n".join(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert transcript (mm:ss) to translated SRT.")
    parser.add_argument("input_file", help="Input transcript file path")
    parser.add_argument("--splits", type=int, default=4, help="Number of splits for parallel translation")
    
    args = parser.parse_args()
    
    processor = ScriptProcessor(args.input_file, args.splits)
    processor.load_and_parse()
    processor.process()
