import os
import json

# 路徑設定
json_root = "./TAT-MOE/TAT-MOE-train/json" # 分別選擇 train/test/eval 的 json 位置
mic_dirs = ["lavalier"] # 領夾麥克風
# ["android", "condenser", "ios", "lavalier", "XYH-6-X", "XYH-6-Y"] # 六種麥克風

# 你想輸出的最終 JSONL 檔案
output_file = "./train.jsonl"
# 音檔的最終路徑前綴
base_audio_path = "./TAT-MOE/TAT-MOE-train" 

with open(output_file, "w", encoding="utf-8") as out_f:
    for speaker_folder in os.listdir(json_root):
        speaker_path = os.path.join(json_root, speaker_folder)
        if not os.path.isdir(speaker_path):
            continue
        
        for json_file in os.listdir(speaker_path):
            if not json_file.endswith(".json"):
                continue
            
            json_path = os.path.join(speaker_path, json_file)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            hanlo_text = data.get("漢羅台文", "").strip() # 可以根據需求選擇"漢羅台文"或"台羅拼音"

            wav_filename = json_file.replace(".json", ".wav")

            for mic in mic_dirs:
                audio_path = os.path.join(base_audio_path, mic, speaker_folder, wav_filename)
                record = {
                    "audio_filepath": audio_path,
                    "text": hanlo_text
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"✅ 已生成 {output_file}")

