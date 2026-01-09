import json
import re

input_file = "./test.jsonl"  # 你的 JSONL 檔案路徑
output_file = "ref_test.txt"

def clean_and_space(text: str) -> str:
    # 去除中英文標點
    text = re.sub(r"[，。！？、,.!?；：「」『』（）《》〈〉—…-]", "", text)
    
    zh_pattern = re.compile(r'[\u4e00-\u9fff]')
    
    result = []
    prev_char = None
    prev_is_zh = False

    for ch in text.strip():
        curr_is_zh = bool(zh_pattern.match(ch))
        # 如果上一字和當前字一方是中文，另一方是非中文，就插空格分隔
        if prev_char is not None:
            if (prev_is_zh != curr_is_zh):
                result.append(" ")
            # 中文跟中文之間也插空格（沿用原本邏輯）
            elif prev_is_zh and curr_is_zh:
                result.append(" ")
        result.append(ch)
        prev_char = ch
        prev_is_zh = curr_is_zh

    return "".join(result)



with open(input_file, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            audio_path = entry["audio_filepath"]
            text = clean_and_space(entry["text"])
            fout.write(f"{audio_path} {text}\n")
        except json.JSONDecodeError:
            print(f"⚠️ 無法解析這行: {line}")
